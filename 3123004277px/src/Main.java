import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        String file1 = "orig.txt";
        String file2 = "orig_add.txt";
        String resultFile = "result.txt";

        try {
            double similarity = calculateCosineSimilarity(file1, file2);
            writeResultToFile(resultFile, similarity);
            System.out.println("重复率计算完成！");
        } catch (IOException e) {
            System.out.println("计算重复率时出现错误：" + e.getMessage());
        }
    }

    public static double calculateCosineSimilarity(String file1, String file2) throws IOException {
        // 读取文件内容
        String content1 = readFileContent(file1);
        String content2 = readFileContent(file2);

        // 分割字符串为单词
        String[] words1 = content1.split("\\s+");
        String[] words2 = content2.split("\\s+");

        // 计算词频向量
        int[] vector1 = calculateWordFrequency(words1);
        int[] vector2 = calculateWordFrequency(words2);

        // 计算余弦相似度
        double dotProduct = calculateDotProduct(vector1, vector2);
        double magnitude1 = calculateMagnitude(vector1);
        double magnitude2 = calculateMagnitude(vector2);

        return dotProduct / (magnitude1 * magnitude2);
    }

    private static String readFileContent(String file) throws IOException {
        StringBuilder content = new StringBuilder();
        BufferedReader reader = new BufferedReader(new FileReader(file));
        String line;

        while ((line = reader.readLine()) != null) {
            content.append(line).append(" ");
        }

        reader.close();
        return content.toString();
    }

    private static int[] calculateWordFrequency(String[] words) {
        int[] frequency = new int[words.length];

        for (int i = 0; i < words.length; i++) {
            frequency[i] = 1;

            for (int j = i + 1; j < words.length; j++) {
                if (words[i].equals(words[j])) {
                    frequency[i]++;
                    words[j] = "";
                }
            }
        }

        return frequency;
    }

    private static double calculateDotProduct(int[] vector1, int[] vector2) {
        double dotProduct = 0;

        for (int i = 0; i < vector1.length; i++) {
            dotProduct += vector1[i] * vector2[i];
        }

        return dotProduct;
    }

    private static double calculateMagnitude(int[] vector) {
        double magnitude = 0;

        for (int value : vector) {
            magnitude += Math.pow(value, 2);
        }

        return Math.sqrt(magnitude);
    }

    private static void writeResultToFile(String file, double similarity) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter(file));
        writer.write("重复率: " + similarity);
        writer.close();
    }
}
