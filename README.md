
# Test Backend Developer

This project is a test for Odoo Backend Developer. Before you deployment this please follow the step


## Deployment


- First you have to copy docker-compose.yml.bak into docker-compose.yml
```bash
sudo cp docker-compose.yml.bak docker-compose.yml
```
- Second you have do the same thing in odoo.conf in folder config
```bash
cd config
sudo cp odoo.conf.bak odoo.conf
```
- Third you have to running the docker-compose.yml
```bash
docker compose up -d
```
- Notes if you're using Linux please chmod 777 in folder data/odoo
```bash
sudo chmod 777 data/odoo
```



## Screenshots

- ### ERD
![ERD](image/ERD_MATERIAL.png)

- ### Application
![APPLICATION](image/FIRST.png)
![](image/SECOND.png)
![](image/THIRD.png)
![](image/FOURTH.png)
![](image/FIFTH.png)

## Tech Stack

**Web:** Odoo version 14

**Database:** Postgresql 14.0
## Authors

- [@nurfachridaffa17](https://www.github.com/nurfachridaffa17)

