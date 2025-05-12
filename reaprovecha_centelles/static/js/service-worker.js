self.addEventListener("install", event => {
    event.waitUntil(
        caches.open("reaprovecha-cache").then(cache => {
            return cache.addAll([
                "/",
                "/static/css/styles.css",
                "/static/img/logo.png"
            ]);
        })
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
