import pytest
from playwright.sync_api import Page, expect
import os
from database import init_database, add_sample_data, seed_test_patrons

# reset database before each run of this file
# since the tests from previous assignments rely
# on the state of the database remaining the same
@pytest.fixture(autouse=True)
def reset_db():
    if os.path.exists('library.db'):
        os.remove('library.db')
    init_database()
    add_sample_data()
    seed_test_patrons()
    yield

BASE_URL = "http://localhost:5000"

@pytest.mark.e2e
def test_add_book_flow(page: Page):
    # navigate to base url
    # press add book
    # fill in the add book form 
    # submit the form
    # check that the book is now in the catalog table


    # navigate to base url
    page.goto(f"{BASE_URL}/catalog")

    # press add book
    page.get_by_role("link", name="➕ Add New Book").click()
    expect(page).to_have_url(f"{BASE_URL}/add_book")

    # fill in the add book form 
    page.fill("#title", "Playwright Book")
    page.fill("#author", "Shakespeare")
    page.fill("#isbn", "5432100000000")
    page.fill("#total_copies", "3")

    # submit the form
    page.get_by_role("button", name="Add Book to Catalog").click()
    expect(page).to_have_url(f"{BASE_URL}/catalog")

    # check that the book is now in the catalog table
    row = page.locator("table tbody tr", has_text="Playwright Book")
    expect(row).to_be_visible()
    expect(row.get_by_text("Shakespeare")).to_be_visible()
    expect(row.get_by_text("5432100000000")).to_be_visible()
    expect(row.get_by_text("3/3 Available")).to_be_visible()



@pytest.mark.e2e
def test_borrow_book_flow(page: Page):
    # navigate to base url
    # fill in the add book form 
    # borrow the book that was added
    # make sure we go back to baseurl/catalog
    # assure that the booking was successful

    # navigate to base url
    page.goto(f"{BASE_URL}/catalog")

    # fill in the add book form 
    page.get_by_role("link", name="➕ Add New Book").click()
    page.fill("#title", "Selenium Sucks")
    page.fill("#author", "Just Kidding")
    page.fill("#isbn", "1230004000009")
    page.fill("#total_copies", "2")
    page.get_by_role("button", name="Add Book to Catalog").click()

    expect(page).to_have_url(f"{BASE_URL}/catalog")

    # borrow the book that was added
    row = page.locator("table tbody tr", has_text="Selenium Sucks")
    #313131 used because they are under the borrow limit
    row.locator("input[name='patron_id']").fill("313131") 
    row.locator("button", has_text="Borrow").click()

    # make sure we go back to baseurl/catalog
    expect(page).to_have_url(f"{BASE_URL}/catalog")

    # assure that the booking was successful
    flash_success = page.locator(".flash-messages")
    expect(flash_success).to_be_visible()
    expect(flash_success).to_contain_text("success", ignore_case=True)


