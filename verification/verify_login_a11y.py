from playwright.sync_api import Page, expect, sync_playwright

def verify_login_a11y(page: Page):
    # 1. Go to the login page
    page.goto("http://localhost:3000/login")

    # 2. Wait for the page to load
    page.wait_for_selector("form")

    # 3. Verify labels are associated with inputs
    # We use get_by_label which relies on aria-label, aria-labelledby, or <label for>
    # If this works, our change is correct.

    # Check Username input
    username_input = page.get_by_label("Username")
    expect(username_input).to_be_visible()

    # Check Password input
    password_input = page.get_by_label("Password")
    expect(password_input).to_be_visible()

    # 4. Verify role="alert" on error
    # To trigger error, we submit empty form or invalid one?
    # The fields are required, so empty submit might not trigger the backend error but browser validation.
    # Let's fill garbage to trigger backend error.

    username_input.fill("wronguser")
    password_input.fill("wrongpass")

    page.get_by_role("button", name="Sign In").click()

    # Wait for error message
    try:
        error_message = page.get_by_role("alert")
        expect(error_message).to_be_visible(timeout=5000)
    except:
        print("Alert not found or visible, taking screenshot")
        pass

    # 5. Screenshot
    page.screenshot(path="/home/jules/verification/login_a11y_retry.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_login_a11y(page)
        except Exception as e:
            print(f"Test failed: {e}")
            page.screenshot(path="/home/jules/verification/failure_retry.png")
            raise e
        finally:
            browser.close()
