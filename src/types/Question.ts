export interface Question {
  questionId: string;
  examYear: string;
  examSeason: string;
  questionNumber: number;
  questionText: string;
  choices: {
    a: string;
    b: string;
    c: string;
    d: string;
  };
  correctAnswer: 'a' | 'b' | 'c' | 'd';
  category: string;
  subcategory: string;
  difficulty: number;
  explanation: string;
}

export type ChoiceKey = 'a' | 'b' | 'c' | 'd';