import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime

from hw11.database.models import Contact, User
from hw11.schemas import ContactModel
from hw11.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.birthday = datetime.strptime("21.11.1999", "%d.%m.%Y")

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_firstname_found(self):
        contact = Contact(first_name="test", last_name="test", email="test@email.com", phone="0000000000", birthday=self.birthday, user=self.user)
        self.session.query().filter().first.return_value = contact
        result = await get_contact(user=self.user, db=self.session, first_name=contact.first_name)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        contact = Contact(first_name="test", last_name="test", email="test@email.com", phone="0000000000", birthday=self.birthday, user=self.user)
        self.session.query().filter().first.return_value = None
        result = await get_contact(user=self.user, db=self.session, first_name=contact.first_name)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name="test", last_name="test", email="test@email.com", phone="0000000000", birthday=self.birthday)
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(first_name="test", last_name="test", email="test@email.com", phone="0000000000", birthday=self.birthday)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(first_name="test", last_name="test", email="test@email.com", phone="0000000000", birthday=self.birthday)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthday_contacts = [
            Contact(birthday=today + timedelta(days=i)) for i in range(5)
        ]
        self.session.query().filter().all.return_value = upcoming_birthday_contacts
        result = await upcoming_birthdays(user=self.user, db=self.session)
        self.assertEqual(len(result), 5)
        for contact in result:
            self.assertTrue(contact.birthday >= today)
            self.assertTrue(contact.birthday <= today + timedelta(days=7))

if __name__ == '__main__':
    unittest.main()
