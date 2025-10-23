self.addEventListener('install', function(event) {
  console.log('Service Worker instalado');
});

self.addEventListener('activate', function(event) {
  console.log('Service Worker ativado');
});

self.addEventListener('fetch', function(event) {
  event.respondWith(fetch(event.request));
});
