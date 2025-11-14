import { collection, getDocs, query, limit } from 'firebase/firestore';
import { db } from '../config/firebase';
import { Question } from '../types/Question';

/**
 * Firestoreから全問題を取得
 */
export const getAllQuestions = async (): Promise<Question[]> => {
  try {
    const questionsRef = collection(db, 'questions');
    const snapshot = await getDocs(questionsRef);
    
    const questions: Question[] = [];
    snapshot.forEach((doc) => {
      questions.push(doc.data() as Question);
    });
    
    return questions;
  } catch (error) {
    console.error('問題の取得に失敗しました:', error);
    throw error;
  }
};

/**
 * Firestoreから指定数の問題を取得（テスト用）
 */
export const getQuestionsLimit = async (limitCount: number): Promise<Question[]> => {
  try {
    const questionsRef = collection(db, 'questions');
    const q = query(questionsRef, limit(limitCount));
    const snapshot = await getDocs(q);
    
    const questions: Question[] = [];
    snapshot.forEach((doc) => {
      questions.push(doc.data() as Question);
    });
    
    return questions;
  } catch (error) {
    console.error('問題の取得に失敗しました:', error);
    throw error;
  }
};