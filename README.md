Video Generator

A powerful web application that converts text from documents (TXT, PDF, DOCX) into professional videos with synchronized audio narration and dynamic text animation.

Project Overview

The Video Generator transforms written content into engaging videos with professional voice narration and synchronized text animations. The system features a modern glassmorphic UI with an animated aurora background and smooth text flowing from center to left.

Key Features

Multi-Format Support
TXT Files: Plain text documents
PDF Files: PDF document extraction
DOCX Files: Microsoft Word documents
Smart Processing: Automatic text extraction and validation

Dynamic Video Generation
Professional Audio: High-quality text-to-speech narration
Synchronized Text: Text flows from center to left with audio
Center-Fixed Current Word: Active word always centered during narration
Smooth Animations: Word-by-word text appearance and movement
No Subtitle Styling: Clean, integrated text display

Modern UI Design
Glassmorphic Design: Frosted glass effect with backdrop blur
Animated Aurora Background: Dynamic color-shifting aurora effect
Responsive Layout: Works on all screen sizes
Smooth Transitions: Hover effects and micro-interactions
Professional Typography: Clean, modern font styling



Technologies Used

Backend
Flask 2.3.3: Web framework for the application
Python 3.7+: Core programming language
OpenCV 4.8.1: Image processing and computer vision
Pillow 10.0.1: Image manipulation and generation
MoviePy 1.0.3: Video editing and composition
NumPy 1.24.3: Numerical computing support
gTTS 2.5.1: Google Text-to-Speech for audio generation
PyPDF2 3.0.1: PDF text extraction
python-docx 0.8.11: Word document processing

Frontend
HTML5: Modern semantic markup
CSS3: Advanced styling with glassmorphism effects
JavaScript: Dynamic interactions and file handling
Responsive Design: Mobile-friendly interface

How It Works

Step 1: File Upload
1. User selects TXT, PDF, or DOCX file
2. File is validated for format and size
3. Text content is extracted using appropriate library

Step 2: Text Processing
1. Text is cleaned and formatted for optimal narration
2. Professional language conversion applied
3. Text is segmented for synchronized animation timing

Step 3: Audio Generation
1. Text is converted to professional speech using gTTS
2. Audio is optimized for clarity and natural delivery
3. Audio duration is calculated for video synchronization

Step 4: Video Creation
1. Text animation frames are generated with center-to-left flow
2. Current word remains centered while previous words flow left
3. Background is created with plain blue color
4. Frames are compiled into MP4 video with integrated audio

Step 5: Output & Download
1. Video is saved to outputs directory
2. Download button appears for easy access
3. Video can be previewed directly in browser

Video Generator - Transform your text into professional videos with synchronized narration and dynamic animations.
