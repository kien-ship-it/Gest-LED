Hello Team,

Welcome to the Gest-LED project! I've set up the repository, and this guide will walk you through everything you need to do to get started using the **GitHub Desktop** application.

Please follow these steps carefully. Using this workflow will prevent errors and make our collaboration smooth.

---

### **Step 1: Clone the Repository to Your Computer**

This step copies the project from GitHub to your local machine. You only need to do this once.

1.  **Open GitHub Desktop.** If you haven't already, log in with your GitHub account.
2.  Go to the menu and click **File > Clone Repository**.
3.  A window will open. Make sure you are on the **GitHub.com** tab. You should see `YourUsername/Gest-LED` in the list. Click on it.
4.  In the "Local Path" field, choose a folder on your computer where you want to save the project (e.g., `C:\GitHub` or `~/Documents/GitHub`).
5.  Click the blue **Clone** button.



You now have a complete copy of the project on your computer!

---

### **Step 2: Your Day-to-Day Workflow**

Follow this cycle every time you start working on a new task.

#### **A. Create Your Branch**

Never work directly on the `main` branch. Always create a new branch for your task.

1.  At the top of the GitHub Desktop window, it will say **Current Branch: `main`**. Click on it.
2.  Click the blue **New Branch** button.
3.  Name your branch using the format `feature/your-name/task-description`.
    *   **Example for Engineer A:** `feature/dang/vision-module-setup`
    *   **Example for Engineer C:** `feature/bao/build-led-circuit-test`
4.  Make sure "Start new branch from:" is set to `main`.
5.  Click **Create Branch**. You are now on your own safe branch.



#### **B. Make and Save Your Code Changes**

1.  Using File Explorer or your code editor (like VS Code or Arduino IDE), navigate to the project folder you created in Step 1.
2.  Find your designated files inside the `src/` folder and start coding.
    *   **Team Alpha:** Work in `src/pc_vision_system/`.
    *   **Team Bravo:** Work in `src/embedded_system/`.
3.  Save your files in your editor as you normally would.

#### **C. Commit Your Changes**

A "commit" is a snapshot of your saved work. Do this frequently.

1.  Switch back to the GitHub Desktop app.
2.  On the left side, you will see a list of all the files you have changed under the **"Changes"** tab.
3.  **Check the boxes** next to the files you want to save in this snapshot.
4.  In the bottom-left corner, write a short, clear summary of the changes you made in the **"Summary"** box. (e.g., "feat: Add initial detector function").
5.  Click the blue **"Commit to [your-branch-name]"** button.



#### **D. Push Your Branch to GitHub**

This uploads your committed changes from your computer to the central GitHub repository.

1.  After you commit, a blue button will appear at the top. The first time, it will say **"Publish branch"**. After that, it will say **"Push origin"**.
2.  Click this button to upload your work.



#### **E. Open a Pull Request (PR)**

When your feature is complete and ready to be merged into the main project, you create a Pull Request.

1.  After you push, a banner will often appear with a button that says **"Create Pull Request"**. This is the easiest way. Click it.
2.  Alternatively, go to the menu and select **Branch > Create Pull Request**.
3.  This will open a new page in your web browser (on GitHub.com).
    *   Write a clear title for your PR.
    *   On the right side, click the gear icon next to "Reviewers" and **assign your partner or the team lead (Engineer B)** to review your code.
    *   Click the green **"Create Pull Request"** button.

Your part is done! Your reviewer will now check your code and merge it when it's ready.

---

### **Step 3: How to Keep Your Branch Updated**

Before you start work each day, or before you create a pull request, you should update your branch with any changes from `main`. This prevents conflicts.

1.  In GitHub Desktop, switch your **Current Branch** to `main`.
2.  Click the **"Fetch origin"** button at the top. If there are new changes, it will turn into a **"Pull origin"** button. Click it to download the latest updates.
3.  Now, switch back to your own feature branch (e.g., `feature/dang/vision-module-setup`).
4.  Go to the menu and select **Branch > Update from main**.
5.  This will bring all the new changes from `main` into your branch safely.



---

### **Golden Rule**

> **NEVER commit directly to the `main` branch.** Always follow the workflow of creating a branch and opening a Pull Request.

Let's get building! Reach out if you have any questions.