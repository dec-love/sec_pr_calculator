#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <iomanip>
#include <sys/stat.h> // ディレクトリ作成用のヘッダー

int main()
{
    int n = 10; // nの値を10に設定
    std::string directory = "p_binominal_result";

    // ディレクトリが存在しない場合は作成
    struct stat info;
    if (stat(directory.c_str(), &info) != 0)
    {
        mkdir(directory.c_str(), 0777); // ディレクトリ作成
    }

    // ファイル名を生成
    std::string filename = directory + "/p_n" + std::to_string(n) + ".csv";
    std::ofstream file(filename);

    // ファイルが開けない場合のエラーハンドリング
    if (!file.is_open())
    {
        std::cerr << "Unable to open file";
        return 1;
    }

    // CSVのヘッダーを書き込む
    file << std::fixed << std::setprecision(4);
    file << "p";
    for (int i = 0; i <= n; i++)
    {
        file << "," << i;
    }
    file << "\n";

    // pを0から1.0まで0.0001刻みで変化させて計算
    file << std::setprecision(8); // 小数点以下8桁に設定
    for (double p = 0.0; p <= 1.0; p += 0.0001)
    {
        file << p;
        for (int i = 0; i <= n; i++)
        {
            double result = std::pow(p, i) * std::pow(1 - p, n - i);
            file << "," << result;
        }
        file << "\n";
    }

    file.close();
    std::cout << "CSV file saved to: " << filename << std::endl;

    return 0;
}
