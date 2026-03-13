from sqlalchemy import update
from sqlalchemy.orm import Session
from app.models.click import Click
from app.models.link import Link
from app.services.links import get_link
import requests

def register_click(db: Session, link: Link, ip: str, device: str) -> Click:
    country_ip = requests.get(f"http://ip-api.com/json/{ip}", params={'fields': 'country'})\
        .json().get('country')
    click = Click(link_id = link.id, country = country_ip, device = device)
    db.add(click)
    # We increment click_count this way to avoid race conditions during concurrent requests
    db.execute(update(Link)
               .where(Link.id == link.id)
               .values(click_count=Link.click_count+1))
    db.commit()
    return click

def get_link_and_register_click(db: Session, slug: str, ip: str, device: str | None) -> Link:
    link = get_link(db, slug)
    register_click(db, link, ip, device)
    return link