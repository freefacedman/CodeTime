#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import re

class ComprehensiveQuestionnaireGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Comprehensive Self-Improvement Questionnaire")
        self.master.geometry("1000x800")
        self.master.configure(bg="#f0f4f7")  # Light background color

        # Apply a modern theme
        style = ttk.Style()
        style.theme_use("clam")  # "clam" is a good base for customization

        # Define a calm color palette
        self.primary_color = "#6c9dcf"   # Soft blue
        self.secondary_color = "#a3c4f3" # Light blue
        self.accent_color = "#88b04b"    # Soft green
        self.background_color = "#f0f4f7" # Light gray-blue
        self.text_color = "#333333"       # Dark gray for text

        # Customize styles
        style.configure("TLabel",
                        background=self.background_color,
                        foreground=self.text_color,
                        font=("Helvetica", 11))
        style.configure("Title.TLabel",
                        background=self.background_color,
                        foreground=self.primary_color,
                        font=("Helvetica", 16, "bold"))
        style.configure("Subtitle.TLabel",
                        background=self.background_color,
                        foreground="#555555",
                        font=("Helvetica", 10))
        style.configure("TButton",
                        font=("Helvetica", 10, "bold"),
                        padding=6,
                        foreground="white",
                        background=self.primary_color)
        style.map("TButton",
                  foreground=[('active', 'white')],
                  background=[('active', self.secondary_color)])
        style.configure("TCombobox",
                        padding=6,
                        relief="flat",
                        font=("Helvetica", 10))
        style.configure("TEntry",
                        font=("Helvetica", 10),
                        padding=5)
        style.configure("TFrame",
                        background=self.background_color)

        # Title Frame
        title_frame = ttk.Frame(self.master)
        title_frame.pack(fill="x", pady=15, padx=20)

        title_label = ttk.Label(
            title_frame,
            text="Comprehensive Self-Improvement Questionnaire",
            style="Title.TLabel"
        )
        title_label.pack()

        instructions_label = ttk.Label(
            title_frame,
            text=(
                "Explore various aspects of your personal and professional life.\n"
                "Navigate through the tabs below, answer the questions, and submit your responses."
            ),
            style="Subtitle.TLabel"
        )
        instructions_label.pack(pady=(5, 0))

        # Notebook for Tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Define all questionnaire sets
        self.QUESTION_SETS = {
            "Relationship Improvement": [
                "1. What should I start doing in our relationship?",
                "2. What should I stop doing in our relationship?",
                "3. What should I keep doing in our relationship?",
                "4. What is one thing I could do to improve our relationship?",
                "5. What is one behavior I should avoid in our relationship?",
                "6. How can I better support you in our relationship?",
                "7. What is one small change I can make to strengthen our relationship?",
                "8. What is one big change I can make to strengthen our relationship?",
                "9. What are the first words that come to mind when describing our relationship?",
                "10. If this was the last time we could be together, what would you want to ask me or tell me?"
            ],
            "Group Project Improvement": [
                "1. What should we start doing as a group to enhance our project’s success?",
                "2. What should we stop doing as a group to avoid setbacks?",
                "3. What should we keep doing as a group to stay on track?",
                "4. What is one thing we can do to improve our communication?",
                "5. What behavior should the team avoid to maintain a positive environment?",
                "6. How can we better support each other in achieving our project goals?",
                "7. What is one small change that could strengthen our teamwork?",
                "8. What is one big change that could significantly improve our project progress?",
                "9. What words best describe our current group dynamic?",
                "10. If this was our last meeting together, what would you want the team to know or remember?"
            ],
            "Mental Health": [
                "1. How are you currently feeling emotionally?",
                "2. What are your primary sources of stress?",
                "3. What activities help you relax and unwind?",
                "4. How do you manage your stress and anxiety?",
                "5. What support systems do you have in place for your mental health?",
                "6. What changes can you make to improve your mental well-being?",
                "7. How do you prioritize self-care in your daily routine?",
                "8. What mental health goals would you like to achieve?",
                "9. How do you cope with negative thoughts or feelings?",
                "10. What additional resources or support do you need for your mental health?"
            ],
            "Problems You Are Facing": [
                "1. What is the main problem you are currently facing?",
                "2. How is this problem affecting your daily life?",
                "3. What steps have you taken to address this problem?",
                "4. What obstacles are preventing you from solving this problem?",
                "5. Who can you reach out to for help with this issue?",
                "6. What resources do you need to overcome this problem?",
                "7. How do you feel about the progress you’ve made so far?",
                "8. What strategies can you implement to tackle this challenge?",
                "9. What have you learned from dealing with this problem?",
                "10. What would success look like in resolving this issue?"
            ],
            "Personal Development": [
                "1. What personal skills would you like to develop?",
                "2. What are your short-term personal goals?",
                "3. What are your long-term aspirations?",
                "4. How do you plan to achieve your personal goals?",
                "5. What habits do you want to build or break?",
                "6. How do you measure your personal growth?",
                "7. What motivates you to improve yourself?",
                "8. What challenges do you face in your personal development journey?",
                "9. Who or what inspires you to grow?",
                "10. What achievements are you most proud of?"
            ],
            "Work-Life Balance": [
                "1. How satisfied are you with your current work-life balance?",
                "2. What factors contribute to your work-life balance?",
                "3. How do you prioritize your professional and personal responsibilities?",
                "4. What challenges do you face in maintaining work-life balance?",
                "5. What strategies do you use to manage your time effectively?",
                "6. How do you ensure you have time for relaxation and leisure?",
                "7. What changes can you make to improve your work-life balance?",
                "8. How does your work-life balance affect your overall well-being?",
                "9. What boundaries do you set between work and personal life?",
                "10. What support do you need to achieve a better work-life balance?"
            ],
            "Career Development": [
                "1. What are your current career goals?",
                "2. What skills do you need to develop to advance in your career?",
                "3. How do you plan to achieve your professional aspirations?",
                "4. What professional achievements are you most proud of?",
                "5. What challenges do you face in your career progression?",
                "6. How do you stay updated with industry trends and knowledge?",
                "7. What networking strategies do you use to expand your professional connections?",
                "8. How do you seek feedback and mentorship in your career?",
                "9. What work experiences have been most valuable to your growth?",
                "10. What changes would you make to better align your career with your personal values?"
            ],
            "Health & Fitness": [
                "1. How would you rate your current physical health?",
                "2. What exercise routines do you follow regularly?",
                "3. How do you incorporate physical activity into your daily life?",
                "4. What dietary habits do you practice to maintain your health?",
                "5. What health-related goals would you like to achieve?",
                "6. How do you monitor and track your fitness progress?",
                "7. What challenges do you face in maintaining a healthy lifestyle?",
                "8. How do you stay motivated to exercise and eat well?",
                "9. What role does sleep play in your overall health?",
                "10. What resources or support do you need to improve your health and fitness?"
            ],
            "Financial Wellness": [
                "1. What are your short-term financial goals?",
                "2. What are your long-term financial aspirations?",
                "3. How do you budget and manage your expenses?",
                "4. What strategies do you use to save money?",
                "5. How do you plan for unexpected financial emergencies?",
                "6. What investments or financial planning have you undertaken?",
                "7. What challenges do you face in achieving financial stability?",
                "8. How do you educate yourself about financial management?",
                "9. What financial habits would you like to develop or change?",
                "10. What resources or support do you need to enhance your financial wellness?"
            ],
            "Social Connections": [
                "1. How would you describe your current relationships with friends and family?",
                "2. How often do you engage in social activities?",
                "3. What steps do you take to maintain and strengthen your relationships?",
                "4. How do you balance your social life with other responsibilities?",
                "5. What challenges do you face in building or maintaining social connections?",
                "6. How do you foster a sense of community in your life?",
                "7. What role do social interactions play in your overall well-being?",
                "8. How do you handle conflicts or misunderstandings in your relationships?",
                "9. What new social connections would you like to develop?",
                "10. What support do you need to enhance your social life and connections?"
            ]
        }

        # Initialize a dictionary to hold user inputs for each questionnaire
        self.user_inputs = {key: [] for key in self.QUESTION_SETS.keys()}

        # Create tabs for each questionnaire
        for questionnaire, questions in self.QUESTION_SETS.items():
            self.create_tab(questionnaire, questions)

        # User Info Frame
        user_frame = ttk.Frame(self.master, padding=10)
        user_frame.pack(fill="x", padx=20, pady=10)

        user_label = ttk.Label(user_frame, text="Your Name/Email:", font=("Helvetica", 11, "bold"))
        user_label.pack(side="left", padx=(0, 10))

        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(user_frame, textvariable=self.user_var, width=40)
        self.user_entry.pack(side="left", padx=(0, 20))

        # Submit Button
        submit_button = ttk.Button(
            user_frame,
            text="Submit All Answers",
            command=self.submit_all_answers
        )
        submit_button.pack(side="left")

    def create_tab(self, questionnaire, questions):
        """
        Create a tab for each questionnaire with its questions.
        """
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=questionnaire)

        # Create a canvas and scrollbar within the tab for scrollable content
        canvas = tk.Canvas(tab, borderwidth=0, background="#f0f4f7")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=10, style="TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store entries for this questionnaire
        self.user_inputs[questionnaire] = []

        # Add questions and answer fields
        for q in questions:
            question_label = ttk.Label(
                scrollable_frame,
                text=q,
                wraplength=900,
                anchor="w",
                justify="left",
                font=("Helvetica", 11),
                background="#f0f4f7",
                foreground=self.primary_color
            )
            question_label.pack(fill="x", pady=(10, 5))

            # Use Text widget for multi-line answers
            answer_text = tk.Text(
                scrollable_frame,
                wrap="word",
                width=100,
                height=3,
                font=("Helvetica", 10),
                bg="#ffffff",
                fg=self.text_color,
                bd=1,
                relief="solid"
            )
            answer_text.pack(fill="x", pady=(0, 10))
            self.user_inputs[questionnaire].append((q, answer_text))

    def sanitize_filename(self, name):
        """
        Sanitize the questionnaire name to create a valid filename.
        Replace spaces and special characters with underscores.
        """
        # Remove any characters that are not letters, numbers, or underscores
        sanitized = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
        return sanitized

    def submit_all_answers(self):
        """
        Collect all answers from all questionnaires, display a summary, and log them to separate files.
        """
        user_info = self.user_var.get().strip()
        if not user_info:
            user_info = "Anonymous"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        overall_summary = [
            f"Timestamp: {timestamp}",
            f"User Info: {user_info}\n"
        ]

        # Create a dictionary to hold summaries per questionnaire for popup
        popup_summaries = []

        for questionnaire, responses in self.user_inputs.items():
            summary_lines = [
                f"--- {questionnaire} ---",
                f"Timestamp: {timestamp}",
                f"User Info: {user_info}\n"
            ]

            for question, text_widget in responses:
                answer = text_widget.get("1.0", "end").strip()
                summary_lines.append(f"{question}\nAnswer: {answer}\n")

            summary_text = "\n".join(summary_lines)
            popup_summaries.append(summary_text)

            # Sanitize the questionnaire name for the filename
            sanitized_name = self.sanitize_filename(questionnaire)
            log_filename = f"{sanitized_name}_log.txt"

            # Ensure the logs directory exists
            os.makedirs("logs", exist_ok=True)
            log_path = os.path.join("logs", log_filename)

            # Write to the respective log file
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(summary_text)
                log_file.write("\n" + "="*80 + "\n\n")  # Divider for readability

        # Combine all summaries for the popup
        combined_popup = "\n".join(popup_summaries)

        # Display the summary in a popup
        messagebox.showinfo("Summary of Responses", combined_popup)

        # Clear all text fields after submission
        for responses in self.user_inputs.values():
            for _, text_widget in responses:
                text_widget.delete("1.0", "end")

        # Clear user info
        self.user_var.set("")

    def log_responses(self, text):
        """
        This method is no longer needed as logging is handled in submit_all_answers.
        Retained for compatibility if needed.
        """
        pass  # Logging is handled within submit_all_answers

def main():
    root = tk.Tk()
    app = ComprehensiveQuestionnaireGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
