import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import ImageClip, AudioFileClip
import tempfile
import uuid
from gtts import gTTS
import random
import math

class VideoGenerator:
    def __init__(self):
        self.output_dir = 'outputs'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_gradient_background(self, width=1920, height=1080):
        """Create a simple plain background"""
        # Simple blue background
        img = Image.new('RGB', (width, height), color=(30, 60, 120))
        return img
    
    def create_animated_text_frames(self, text, width=1280, height=720, duration=8):
        """Create frames with text flowing from center to left, current word always centered"""
        words = text.split()
        frames = []
        fps = 12
        total_frames = int(duration * fps)
        
        # Try to use a nice font
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        
        # Create frames with smooth text flow from center to left
        for frame_idx in range(total_frames):
            # Create background
            img = self.create_gradient_background(width, height)
            draw = ImageDraw.Draw(img)
            
            # Calculate progress (0 to 1)
            progress = frame_idx / total_frames
            
            # Calculate which word is currently being spoken
            current_word_idx = int(progress * len(words))
            current_word_idx = min(current_word_idx, len(words) - 1)
            
            # Always show text after initial frames (avoid empty screen issues)
            if progress < 0.05:  # First 5% - empty screen
                pass
            else:
                # Get current word and previous words
                current_word = words[current_word_idx] if current_word_idx < len(words) else words[-1]
                previous_words = words[:current_word_idx]
                
                # Center position for current word
                center_x = width // 2
                center_y = height // 2
                
                # Calculate current word dimensions
                current_word_bbox = draw.textbbox((0, 0), current_word, font=font)
                current_word_width = current_word_bbox[2] - current_word_bbox[0]
                current_word_height = current_word_bbox[3] - current_word_bbox[1]
                
                # Position current word at center (always fixed)
                current_word_x = center_x - current_word_width // 2
                current_word_y = center_y - current_word_height // 2
                
                # Draw current word at center (bright white)
                draw.text((current_word_x, current_word_y), current_word, fill=(255, 255, 255), font=font)
                
                # Draw previous words flowing to the left
                if previous_words:
                    # Build previous text in order
                    previous_text = ' '.join(previous_words)
                    
                    # Calculate previous text dimensions
                    prev_bbox = draw.textbbox((0, 0), previous_text, font=font)
                    prev_width = prev_bbox[2] - prev_bbox[0]
                    prev_height = prev_bbox[3] - prev_bbox[1]
                    
                    # Position previous text to the left of current word
                    prev_x = current_word_x - prev_width - 30  # 30px gap
                    prev_y = center_y - prev_height // 2
                    
                    # Draw previous text in gray (faded)
                    draw.text((prev_x, prev_y), previous_text, fill=(180, 180, 180), font=font)
            
            # Add minimal debug info (can be removed)
            draw.text((10, 10), f"Word: {current_word_idx + 1}/{len(words)}", fill=(255, 255, 255), font=ImageFont.load_default())
            
            frames.append(img)
        
        return frames
    
    def create_audio(self, text, lang='en'):
        """Generate professional audio from text"""
        try:
            # Use professional, clear text
            professional_text = self.make_professional(text)
            
            # Generate speech with professional pace
            tts = gTTS(text=professional_text, lang=lang, slow=False)
            
            # Save to temporary file
            temp_audio_path = os.path.join(self.output_dir, f'temp_audio_{uuid.uuid4().hex[:8]}.mp3')
            tts.save(temp_audio_path)
            
            # Estimate duration based on text length (professional pace)
            word_count = len(professional_text.split())
            estimated_duration = max(word_count / 140.0 * 60, 5)  # 140 words per minute for professional delivery
            
            return temp_audio_path, estimated_duration
            
        except Exception as e:
            print(f"Audio generation failed: {str(e)}")
            return None, 5  # Return default duration if audio fails
    
    def make_professional(self, text):
        """Convert text to professional, formal language"""
        # Professional replacements
        professional_replacements = {
            "hey there": "hello",
            "what's up": "welcome",
            "check this out": "please note",
            "you gotta": "you should",
            "super": "very",
            "awesome": "excellent",
            "fantastic": "outstanding",
            "cool": "impressive",
            "thanks a bunch": "thank you",
            "if you could": "please",
            "you know": "",
            "pretty cool huh": "",
            "!": ".",
            "gonna": "going to",
            "wanna": "want to",
            "kinda": "somewhat",
            "sorta": "somewhat"
        }
        
        professional_text = text
        
        # Apply professional replacements
        for casual, formal in professional_replacements.items():
            professional_text = professional_text.replace(casual, formal)
        
        # Clean up multiple spaces and ensure proper capitalization
        professional_text = ' '.join(professional_text.split())
        
        # Ensure proper sentence structure
        if professional_text and professional_text[0].islower():
            professional_text = professional_text[0].upper() + professional_text[1:]
        
        # Remove trailing informalities
        professional_text = professional_text.rstrip()
        if not professional_text.endswith(('.', '!', '?')):
            professional_text += '.'
        
        return professional_text
    
    def create_video(self, text, duration=5):
        """Generate an animated video with creative background, text highlighting, and enhanced audio"""
        try:
            # Generate audio first to get duration
            audio_path, audio_duration = self.create_audio(text)
            
            # Use audio duration or default (shorter for faster processing)
            video_duration = audio_duration if audio_path else max(duration, 6)
            
            # Create animated text frames for all texts
            frames = self.create_animated_text_frames(text, duration=video_duration)
            
            # Save frames to temporary files
            frame_paths = []
            for i, frame in enumerate(frames):
                frame_path = os.path.join(self.output_dir, f'frame_{uuid.uuid4().hex[:8]}_{i:04d}.png')
                frame.save(frame_path)
                frame_paths.append(frame_path)
            
            # Generate unique filename
            filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
            output_path = os.path.join(self.output_dir, filename)
            
            # Create video from frames
            try:
                # Use ImageClip for each frame and concatenate
                clips = []
                for frame_path in frame_paths:
                    clip = ImageClip(frame_path, duration=1/12)  # 12 FPS
                    clips.append(clip)
                
                # Concatenate all clips
                from moviepy import concatenate_videoclips
                video_clip = concatenate_videoclips(clips)
                
                # Add audio if available
                if audio_path and os.path.exists(audio_path):
                    try:
                        audio_clip = AudioFileClip(audio_path)
                        final_clip = video_clip.with_audio(audio_clip)
                        
                        # Write video with audio
                        final_clip.write_videofile(
                            output_path, 
                            fps=12,  # Reduced FPS
                            codec='libx264', 
                            audio_codec='aac'
                        )
                        
                        audio_clip.close()
                    except Exception as e:
                        print(f"Audio integration failed: {str(e)}")
                        # Fallback to video without audio
                        video_clip.write_videofile(output_path, fps=12, codec='libx264')
                else:
                    # Create video without audio
                    video_clip.write_videofile(output_path, fps=12, codec='libx264')
                
                video_clip.close()
                
            except Exception as e:
                print(f"Frame-based video creation failed: {str(e)}")
                # Fallback to simple video
                self.create_simple_video(text, output_path, audio_path, video_duration)
            
            # Clean up temporary files
            for frame_path in frame_paths:
                if os.path.exists(frame_path):
                    os.unlink(frame_path)
            
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error creating video: {str(e)}")
    
    def create_simple_video(self, text, output_path, audio_path, duration):
        """Fallback simple video creation with gradient background"""
        # Create single frame with gradient background
        img = self.create_gradient_background(1280, 720)
        
        # Add text
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1280 - text_width) // 2  # Match optimized width
        y = (720 - text_height) // 2   # Match optimized height
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Save and create video
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)
            tmp_path = tmp.name
        
        video_clip = ImageClip(tmp_path, duration=duration)
        
        # Add audio if available
        if audio_path and os.path.exists(audio_path):
            try:
                audio_clip = AudioFileClip(audio_path)
                final_clip = video_clip.with_audio(audio_clip)
                final_clip.write_videofile(output_path, fps=12, codec='libx264', audio_codec='aac')
                audio_clip.close()
            except Exception as e:
                print(f"Audio integration failed: {str(e)}")
                video_clip.write_videofile(output_path, fps=12, codec='libx264')
        else:
            video_clip.write_videofile(output_path, fps=12, codec='libx264')
        
        video_clip.close()
        os.unlink(tmp_path)
