nanoinvoice
===========

Invoicing app

## To compile scss files:

sass --watch screen.scss:../../dist/css/screen.css

## BIND config to test subdomains:

 ;
 ; BIND data file for local loopback interface
 ;
 $TTL    604800
 @       IN      SOA     nanoinvoice.dev. root.nanoinvoice.dev. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
 ;
 @       IN      NS      nanoinvoice.dev.
 @       IN      A       127.0.0.1
 *       IN      A       127.0.0.1
 @       IN      AAAA    ::1


