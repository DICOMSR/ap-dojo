# CLAUDE.md - AP道場 Development Guide

## Project Overview

**AP道場 (AP Dojo)** is a React Native mobile application for practicing **Applied Information Technology Engineer Examination (応用情報技術者試験)** questions. The app provides a comprehensive question bank with past exam questions from 2009 (H21) to 2025 (R07), totaling over 34 exam sessions.

### Key Features
- Browse and practice past exam questions
- Questions organized by category, subcategory, and difficulty
- Integrated with Firebase (Firestore for data, Authentication for users)
- Comprehensive data processing pipeline for exam PDF parsing

---

## Technology Stack

### Frontend/Mobile App
- **React Native**: 0.82.1
- **Expo**: ~54.0.23
- **TypeScript**: ~5.9.2
- **React**: 19.2.0
- **React Navigation**: 7.x (native-stack for navigation)
- **AsyncStorage**: For local data persistence

### Backend/Data
- **Firebase**:
  - Firestore: Database for questions
  - Firebase Auth: User authentication
- **Python**: Data processing scripts for PDF parsing and Firebase upload

### Package Management
- **Yarn**: Primary package manager (yarn.lock present)

---

## Repository Structure

```
ap-dojo/
├── src/                          # Main application source code
│   ├── config/
│   │   └── firebase.ts          # Firebase configuration and initialization
│   ├── screens/
│   │   ├── HomeScreen.tsx       # Main home screen
│   │   └── QuestionListScreen.tsx # Question list display
│   ├── services/
│   │   └── questionService.ts   # Firestore question fetching logic
│   └── types/
│       └── Question.ts          # TypeScript interfaces for questions
│
├── data-processing/              # Python scripts for data pipeline
│   ├── download_ipa_exams.py    # Download exam PDFs from IPA website
│   ├── parse_pdf.py             # Parse PDFs into structured JSON
│   ├── parse_pdf_ocr.py         # OCR-based PDF parsing
│   ├── parse_pdf_tesseract.py   # Tesseract-based PDF parsing
│   ├── upload_to_firebase.py    # Upload parsed questions to Firestore
│   ├── clear_firestore.py       # Clear Firestore database
│   ├── fix_answers.py           # Fix answer formatting issues
│   ├── debug_pdf.py             # Debug PDF parsing
│   ├── debug_matching.py        # Debug answer matching
│   ├── parsed_questions/        # Parsed JSON output (34 exam sessions)
│   ├── outputs/                 # Processing outputs
│   ├── downloaded_pdfs/         # Downloaded exam PDFs
│   └── serviceAccountKey.json   # Firebase Admin SDK credentials (GITIGNORED)
│
├── test-app/                     # Expo template app (for testing/reference)
│   ├── app/                     # Expo Router structure
│   ├── components/              # Reusable components
│   ├── hooks/                   # Custom React hooks
│   └── constants/               # Theme and constants
│
├── .expo/                        # Expo build artifacts
├── poppler/                      # PDF processing library
├── package.json                  # Root package dependencies
├── tsconfig.json                 # TypeScript configuration
├── yarn.lock                     # Yarn dependency lock file
└── README.md                     # Project README (Japanese)
```

---

## Key Conventions

### TypeScript/Code Style

1. **Type Definitions**: All interfaces are defined in `/src/types/`
   - Questions follow the `Question` interface with strict typing
   - Use union types for choice keys: `'a' | 'b' | 'c' | 'd'`

2. **File Naming**:
   - React components: PascalCase with `.tsx` extension (e.g., `HomeScreen.tsx`)
   - Services/utilities: camelCase with `.ts` extension (e.g., `questionService.ts`)
   - Python scripts: snake_case with `.py` extension (e.g., `upload_to_firebase.py`)

3. **Component Structure**:
   - Functional components with hooks (useState, useEffect)
   - StyleSheet.create for styling (no inline styles)
   - Use React Navigation props typing with `any` (consider improving)

4. **Japanese Language**:
   - UI text, comments, and console logs are primarily in Japanese
   - Variable names and function names are in English
   - Keep this convention for consistency

### Firebase Configuration

**IMPORTANT SECURITY NOTE**: The Firebase configuration in `src/config/firebase.ts` contains public API keys. While this is normal for client-side Firebase, ensure:
- `serviceAccountKey.json` is NEVER committed (currently gitignored)
- Firebase Security Rules are properly configured
- Admin operations only happen server-side

```typescript
// Firebase config structure (src/config/firebase.ts)
export const db = getFirestore(app);
export const auth = getAuth(app);
```

### Question Data Model

```typescript
interface Question {
  questionId: string;        // Unique ID (e.g., "H21_春期_Q01")
  examYear: string;          // Year (e.g., "H21", "R07")
  examSeason: string;        // Season: "春期" or "秋期"
  questionNumber: number;    // Question number (1-80)
  questionText: string;      // Question text
  choices: {                 // Multiple choice options
    a: string;
    b: string;
    c: string;
    d: string;
  };
  correctAnswer: 'a' | 'b' | 'c' | 'd';
  category: string;          // Main category
  subcategory: string;       // Subcategory
  difficulty: number;        // Difficulty level
  explanation: string;       // Answer explanation
}
```

---

## Development Workflows

### 1. Mobile App Development

**Starting the development server**:
```bash
# From root directory
yarn install
expo start

# Or specific platform
expo start --ios
expo start --android
expo start --web
```

**File locations for common tasks**:
- Add new screen: Create in `/src/screens/`
- Add new service: Create in `/src/services/`
- Update types: Modify `/src/types/Question.ts`
- Update Firebase config: Modify `/src/config/firebase.ts`

### 2. Data Processing Pipeline

The data pipeline follows these steps:

**Step 1: Download Exam PDFs**
```bash
cd data-processing
python download_ipa_exams.py
```
- Downloads PDFs from IPA website to `downloaded_pdfs/`
- Covers 34 exam sessions (H21-R07, 春期/秋期)

**Step 2: Parse PDFs to JSON**
```bash
python parse_pdf.py
# or alternative parsers:
# python parse_pdf_ocr.py
# python parse_pdf_tesseract.py
```
- Parses PDFs into structured JSON
- Outputs to `parsed_questions/` directory
- Creates `all_questions.json` with combined data

**Step 3: Upload to Firebase**
```bash
python upload_to_firebase.py
```
- Requires `serviceAccountKey.json` in data-processing directory
- Uploads all questions to Firestore `questions` collection
- Shows progress with detailed logging

**Utility Scripts**:
- `clear_firestore.py`: Clear all questions from Firestore
- `fix_answers.py`: Fix answer formatting issues
- `debug_pdf.py`: Debug PDF parsing issues
- `debug_matching.py`: Debug answer matching logic

### 3. Firebase Setup

**Required credentials**:
- Web config: Already in `src/config/firebase.ts` (safe for client-side)
- Admin SDK: Download from Firebase Console → Project Settings → Service Accounts
  - Save as `data-processing/serviceAccountKey.json`
  - **NEVER commit this file**

**Collections**:
- `questions`: All exam questions (indexed by questionId)

---

## Common Tasks for AI Assistants

### Adding a New Screen

1. Create component in `/src/screens/NewScreen.tsx`
2. Follow existing screen patterns (HomeScreen, QuestionListScreen)
3. Use StyleSheet.create for styles
4. Add navigation typing if using React Navigation
5. Use Japanese for UI text, English for code

### Modifying Question Data Structure

1. Update interface in `/src/types/Question.ts`
2. Update parsing scripts in `data-processing/`
3. Update service methods in `/src/services/questionService.ts`
4. Update UI components that display questions
5. Re-run data pipeline to regenerate JSON

### Adding New Data Processing

1. Create script in `data-processing/` with descriptive name
2. Follow existing patterns (verbose logging, error handling)
3. Test with sample data before full dataset
4. Document script purpose at top of file (Japanese comments OK)

### Debugging Firebase Issues

1. Check Firebase console for security rules
2. Verify `serviceAccountKey.json` exists for admin operations
3. Check network connectivity
4. Review console logs (console.log/console.error)
5. Use `debug_*.py` scripts for data issues

### Testing Changes

1. **Mobile app**: Use Expo Go app or simulator
   ```bash
   expo start
   # Scan QR code with Expo Go (mobile)
   # Press 'i' for iOS simulator
   # Press 'a' for Android emulator
   ```

2. **Data processing**: Test with small datasets first
   ```bash
   # Use sample_questions.json instead of all_questions.json
   python upload_to_firebase.py
   ```

---

## Git Workflow

### Branch Naming Convention
- Feature branches: `claude/claude-md-*` (as seen in current development)
- Always develop on designated feature branches
- Never push to main without approval

### Commit Messages
- Use descriptive messages in English or Japanese
- Example: "11/14ここまで" (current style)
- For AI assistants: Use clear, descriptive English messages

### .gitignore Important Files
- `node_modules/`
- `serviceAccountKey.json` (CRITICAL - contains Firebase admin credentials)
- Build artifacts and cached files

---

## Important Notes for AI Assistants

### Security Considerations
1. **NEVER commit** `serviceAccountKey.json`
2. **NEVER expose** Firebase Admin SDK credentials
3. Client-side Firebase config in `firebase.ts` is safe (public API keys)
4. Always check Firebase Security Rules before deploying

### Code Quality
1. Maintain TypeScript strict typing
2. Follow existing patterns for consistency
3. Keep Japanese UI text for user-facing content
4. Use English for code, comments about logic
5. Test Firebase operations before committing

### Testing
1. Test with Expo development server before building
2. Verify Firebase operations with small datasets
3. Check cross-platform compatibility (iOS/Android/Web)
4. Validate question data structure matches interface

### Common Pitfalls
1. **Python environment**: Ensure Firebase Admin SDK is installed
   ```bash
   pip install firebase-admin
   ```

2. **React Native dependencies**: Always use `yarn install`, not npm

3. **Navigation**: Use React Navigation correctly with proper typing

4. **Firestore queries**: Remember to handle async operations properly

5. **PDF parsing**: Different parsers for different PDF formats (try all three if one fails)

---

## Quick Reference Commands

```bash
# Mobile App Development
yarn install                 # Install dependencies
expo start                   # Start development server
expo start --ios            # Start on iOS simulator
expo start --android        # Start on Android emulator

# Data Processing
cd data-processing
python download_ipa_exams.py    # Download PDFs
python parse_pdf.py             # Parse to JSON
python upload_to_firebase.py    # Upload to Firebase
python clear_firestore.py       # Clear database

# Git Operations
git status                   # Check status
git add .                    # Stage all changes
git commit -m "message"      # Commit changes
git push -u origin <branch>  # Push to remote
```

---

## Project Status

**Current State** (as of 2025-11-14):
- ✅ Data processing pipeline complete (34 exam sessions)
- ✅ Firebase integration working
- ✅ Basic screens implemented (Home, QuestionList)
- 🔄 Additional features in development
- 📱 Test app available for reference

**Known Locations**:
- Main app source: `/src`
- Data processing: `/data-processing`
- Parsed questions: `/data-processing/parsed_questions` (all_questions.json has full dataset)
- Test/reference app: `/test-app`

---

## Additional Resources

- Firebase Project: `ap-dojo-6e565`
- IPA Exam Information: https://www.ipa.go.jp/shiken/
- Expo Documentation: https://docs.expo.dev/
- React Navigation: https://reactnavigation.org/

---

**Last Updated**: 2025-11-14
**Maintained by**: AI Development Assistant
