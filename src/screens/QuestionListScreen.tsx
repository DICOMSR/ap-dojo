import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { getAllQuestions } from '../services/questionService';
import { Question } from '../types/Question';

export default function QuestionListScreen({ navigation }: any) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await getAllQuestions();
      // 問題番号でソート
      data.sort((a, b) => a.questionNumber - b.questionNumber);
      setQuestions(data);
    } catch (error) {
      console.error('問題の読み込みに失敗:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderQuestion = ({ item }: { item: Question }) => (
    <TouchableOpacity
      style={styles.questionItem}
      onPress={() => navigation.navigate('QuestionDetail', { question: item })}
    >
      <View style={styles.questionHeader}>
        <Text style={styles.questionNumber}>問{item.questionNumber}</Text>
        <Text style={styles.category}>{item.category}</Text>
      </View>
      <Text style={styles.questionText} numberOfLines={2}>
        {item.questionText}
      </Text>
      <View style={styles.questionFooter}>
        <Text style={styles.subcategory}>{item.subcategory}</Text>
        <Text style={styles.difficulty}>難易度: {item.difficulty}</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>問題を読み込み中...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={questions}
        renderItem={renderQuestion}
        keyExtractor={(item) => item.questionId}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  listContainer: {
    padding: 10,
  },
  questionItem: {
    backgroundColor: 'white',
    padding: 15,
    marginBottom: 10,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  questionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  questionNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  category: {
    fontSize: 12,
    color: '#666',
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  questionText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 10,
    lineHeight: 20,
  },
  questionFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  subcategory: {
    fontSize: 12,
    color: '#999',
  },
  difficulty: {
    fontSize: 12,
    color: '#FF9500',
  },
});