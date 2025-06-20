# AI Assessment Tool (Web App Version)

## Description

This tool provides an initial assessment of projects based on various criteria, accessed via a conversational web interface. Users can input project details through a chat-like system, and the tool offers evaluations on aspects like survivability and current valuation, along with strategic recommendations.

This project evolved from a command-line based assessment tool to a more interactive web application.

## Current Features

-   **Web-Based Interface:** Project details are entered through a web page styled to resemble a chat conversation.
-   **Conversational Data Input:** The system guides the user to provide necessary project details step-by-step.
-   **Implemented Assessment Modules:**
    -   **Survivability Assessment:** Evaluates potential for continued success based on factors like market size and competition.
    -   **Current Valuation Assessment:** Offers a qualitative valuation and a confidence score based on investment, revenue stage, etc.
-   **Placeholder Assessment Modules:** Framework exists for future implementation of:
    -   Popularity Rating
    -   Property Assessment
    -   Business Assessment
    -   Personality Assessment
    -   Psychology Assessment
-   **Recommendation Engine:** Generates basic strategic recommendations from the outputs of the implemented assessment modules.
-   **Basic UI Styling:** The web interface has initial styling for a better user experience.

## How to Run

1.  **Prerequisites:**
    -   Python 3.x
    -   Flask: Install using pip: \`pip install Flask\`
    -   (Optional, for future NLU enhancements): spaCy and a model like \`en_core_web_sm\`.

2.  **Navigate to the Web App Directory:**
    \`\`\`bash
    cd ai_assessment_tool/web_frontend
    \`\`\`

3.  **Run the Flask Application:**
    \`\`\`bash
    python app.py
    \`\`\`

4.  **Access the Application:**
    Open your web browser and go to: \`http://localhost:8080\` (or the address shown in your terminal).

## Project Structure Overview

-   \`README.md\`: This file.
-   \`.gitignore\`: Specifies intentionally untracked files that Git should ignore.
-   \`LICENSE\`: Contains the license for the project (currently the default from the initial setup).
-   \`requirements.txt\`: Basic dependencies (primarily Flask for the web app).
-   \`ai_assessment_tool/\`: Main Python package for the assessment logic and web app.
    -   \`assessments/\`: Contains individual modules for different types of assessments (e.g., \`survivability.py\`, \`valuation.py\`).
    -   \`core/data_structures.py\`: Defines core Python objects like \`ProjectInput\` and \`AssessmentOutput\`.
    -   \`recommendation_engine.py\`: Logic for generating recommendations based on assessment scores.
    -   \`chatbot_engine/\`: (Future Development) Intended for Natural Language Understanding (NLU) and more advanced chatbot interaction logic.
        -   \`nlu_service.py\`: Placeholder for NLU parsing.
    -   \`web_frontend/\`: Contains the Flask web application.
        -   \`app.py\`: The main Flask application file with routes and web logic.
        -   \`static/style.css\`: CSS stylesheet for the web interface.
        -   \`templates/\`: HTML templates used by Flask.
            -   \`index_chat.html\`: Main page for the chat-like input.
            -   \`result_chat.html\`: Page to display assessment results.
-   \`src/\` and \`tests/\` (root level): These relate to an earlier, simpler word counting tool and are not part of the AI Assessment Web App. They could be removed or moved to a separate example folder.

## Future Development Ideas

-   **Implement Placeholder Modules:** Flesh out the logic for Popularity, Property, Business, Personality, and Psychology assessments.
-   **True NLU/Chatbot Integration:** Replace the current rule-based input parsing with a more robust NLU engine (e.g., using spaCy as outlined in \`chatbot_engine/nlu_service.py\`) for more natural conversation.
-   **Database Integration:** Store project assessments, user details (if applicable), and potentially chat histories.
-   **Advanced UI/UX:**
    -   Implement asynchronous communication for a true real-time chat feel.
    -   Add user accounts and authentication.
    -   Improve visual design and responsiveness further.
-   **Expand Recommendation Engine:** Make recommendations more nuanced and context-aware.
-   **Testing:** Add more comprehensive unit and integration tests, especially for the web frontend and parsing logic.

EOL
