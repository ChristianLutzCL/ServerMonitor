// This is based on the First Progressive Web App Tutorial by Google
// https://codelabs.developers.google.com/codelabs/your-first-pwapp/
const cacheName = 'flask-PWA-v3';
const filesToCache = [
    'offline.html'
];

// When the 'install' event is fired we will cache
// the html, javascript, css, images and any other files important
// to the operation of the application shell
self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});

// We then listen for the service worker to be activated/started. Once it is
// ensures that your service worker updates its cache whenever any of the app shell files change.
// In order for this to work, you'd need to increment the cacheName variable at the top of this service worker file.
self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
    e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});


// Serve the app shell from the cache
// If the file is not in the cache then try to get it via the network.
// otherwise give an error and display an offline page
// This is a just basic example, a better solution is to use the
// Service Worker Precache module https://github.com/GoogleChromeLabs/sw-precache
self.addEventListener('fetch', function(e) {
  console.log('[ServiceWorker] Fetch', e.request.url);
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request).catch(error => {
          console.log('Fetch failed; returning offline page instead.', error);

          // In reality you'd have many different
          // fallbacks, depending on URL & headers.
          // Eg, a fallback silhouette image for avatars.
          let url = e.request.url;
          let extension = url.split('.').pop();

          if (extension === 'jpg' || extension === 'png') {

              const FALLBACK_IMAGE = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="180" stroke-linejoin="round">
                <path stroke="#DDD" stroke-width="25" d="M99,18 15,162H183z"/>
                <path stroke-width="17" fill="#FFF" d="M99,18 15,162H183z" stroke="#eee"/>
                <path d="M91,70a9,9 0 0,1 18,0l-5,50a4,4 0 0,1-8,0z" fill="#aaa"/>
                <circle cy="138" r="9" cx="100" fill="#aaa"/>
                </svg>`;
              // const FALLBACK_IMAGE = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path class="heroicon-ui" d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6c0-1.1.9-2 2-2zm16 8.59V6H4v6.59l4.3-4.3a1 1 0 0 1 1.4 0l5.3 5.3 2.3-2.3a1 1 0 0 1 1.4 0l1.3 1.3zm0 2.82l-2-2-2.3 2.3a1 1 0 0 1-1.4 0L9 10.4l-5 5V18h16v-2.59zM15 10a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>`;
              return Promise.resolve(new Response(FALLBACK_IMAGE, {
                  headers: {
                      'Content-Type': 'image/svg+xml'
                  }
              }));
          }

          // Then we can have a default fallback for web pages to show an offline page
          return caches.match('offline.html');
      });
    })
  );
});