# Nginx Knowledge Summary

**Proficiency:** Basic → Working  
**Last Studied:** 2026-03-26

---

## What is Nginx?

Nginx is a high-performance web server and reverse proxy server. It handles HTTP/HTTPS requests, SSL termination, load balancing, and serves static files efficiently.

### Why Nginx for Zer0Day Labs?

1. **Reverse Proxy** - Routes requests to Next.js apps (MusicGen, AudioStudio)
2. **SSL/TLS Termination** - Handles encryption, offloads from apps
3. **Caching** - Serves static assets directly (improves performance)
4. **Load Balancing** - Distributes traffic across multiple instances
5. **Security** - Rate limiting, DDoS protection, header manipulation

---

## Core Configuration Patterns

### 1. Basic Reverse Proxy for Next.js

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve static files directly
    location /_next/static {
        alias /path/to/your/nextjs/app/.next/static;
        expires 365d;
        access_log off;
    }
}
```

### 2. SSL/TLS with Let's Encrypt

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

**Install certbot:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 3. Performance Optimizations

```nginx
# Gzip compression
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Cache static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 365d;
    add_header Cache-Control "public, no-transform";
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

location / {
    limit_req zone=one burst=20;
    proxy_pass http://localhost:3000;
}
```

---

## Commands & Maintenance

### Basic Operations
```bash
sudo nginx -t           # Test configuration
sudo systemctl start nginx
sudo systemctl reload nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

### Logs & Monitoring
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check active connections
nginx -s status
```

### Certbot (SSL)
```bash
# Renew certificates
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal
```

---

## Common Use Cases at Zer0Day Labs

1. **MusicGen (edmmusic.studio)** - Would use Nginx as reverse proxy
2. **AudioStudio (audiostudio.ai)** - Would use Nginx as reverse proxy
3. **Vercel deployment** - Currently uses Vercel's built-in hosting, but Nginx could be used for custom domains

### Why Not Deploy Nginx Now?

- **Vercel handles** reverse proxy, SSL, caching, CDN automatically
- **Railway DBs** not connected yet - need infrastructure integration first
- **Current pattern:** Vercel deployment is simpler and fully managed
- **Future use:** Could deploy self-hosted Nginx if cost optimization or custom requirements arise

---

## Nginx Best Practices

1. **Always test configs** before reload: `nginx -t`
2. **Use HTTP to HTTPS redirect** for security
3. **Enable gzip compression** for all text assets
4. **Cache static files** aggressively (365 days for hashed assets)
5. **Set proper headers** for reverse proxy (X-Real-IP, X-Forwarded-For)
6. **Rate limit** public endpoints to prevent abuse
7. **Monitor logs** regularly for errors
8. **Automate SSL** with Certbot auto-renewal

---

## Resources

- [NGINX Official Documentation](https://nginx.org/en/docs/)
- [Next.js Deployment](https://nextjs.org/docs/app/building-your-application/deploying)
- [Let's Encrypt Docs](https://letsencrypt.org/docs/)
- [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)
- [Web Performance Optimization](https://web.dev/performance/)

---

## Key Takeaways

✅ **Nginx = Reverse proxy + SSL termination + Static file serving**  
✅ **For Next.js: proxy_pass to port 3000, serve /_next/static directly**  
✅ **Let's Encrypt = free SSL, auto-renewal**  
✅ **Vercel handles all this automatically** - current deployment pattern works  
✅ **Could self-host with Nginx if needed** for cost optimization later
