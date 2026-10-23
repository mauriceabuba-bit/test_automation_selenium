
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_URL = (PROJECT_ROOT / "index.html").as_uri()

HOME_TEXT = "Home"
ABOUT_TEXT = "About"
SKILLS_TEXT = "Skills"
PROJECTS_TEXT = "Projects"
CONTACT_TEXT = "Contact"

HOME_URL = TEST_URL + "#home"
ABOUT_URL = TEST_URL + "#about"
SKILLS_URL = TEST_URL + "#skills"
PROJECTS_URL = TEST_URL + "#projects"
CONTACT_URL = TEST_URL + "#contact"
