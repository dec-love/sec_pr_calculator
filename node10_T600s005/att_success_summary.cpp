#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>

// データを格納するための構造体を定義
struct Data
{
    double s;
    int i;
    int success;
    int success2; // 新たに追加
};

// ファイル名から保存名を生成する関数
std::string generateOutputFilename(const std::string &inputFilename)
{
    size_t lastDot = inputFilename.find_last_of(".");
    if (lastDot == std::string::npos)
    {
        return inputFilename + "_summary";
    }
    return inputFilename.substr(0, lastDot) + "_summary" + inputFilename.substr(lastDot);
}

int main()
{
    // 入力ファイル名
    std::string inputFilename = "att_result/att_n10_delay5_T600.csv";
    // 出力ファイル名を生成
    std::string outputFilename = generateOutputFilename(inputFilename);

    // ファイルの読み込み
    std::ifstream inputFile(inputFilename);
    std::ofstream outputFile(outputFilename);

    if (!inputFile.is_open())
    {
        std::cerr << "Failed to open input file" << std::endl;
        return 1;
    }

    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open output file" << std::endl;
        return 1;
    }

    // データ構造を初期化
    std::map<std::pair<double, int>, std::tuple<int, int, int, int>> results; // success, false, success2, false2

    std::string line;
    std::getline(inputFile, line); // ヘッダー行をスキップ

    while (std::getline(inputFile, line))
    {
        std::istringstream iss(line);
        std::string token;
        Data data;

        // 行からデータを解析
        std::getline(iss, token, ',');
        data.s = std::stod(token);

        std::getline(iss, token, ',');
        data.i = std::stoi(token);

        // binary, staleRate, advMax, adv 列をスキップ
        for (int j = 0; j < 4; ++j)
        {
            std::getline(iss, token, ',');
        }

        std::getline(iss, token, ',');
        data.success = std::stoi(token);

        std::getline(iss, token, ',');
        data.success2 = std::stoi(token); // 新たに追加

        auto key = std::make_pair(data.s, data.i);
        if (data.success == 1)
        {
            std::get<0>(results[key])++; // successカウント
        }
        else
        {
            std::get<1>(results[key])++; // falseカウント
        }

        if (data.success2 == 1)
        {
            std::get<2>(results[key])++; // success2カウント
        }
        else
        {
            std::get<3>(results[key])++; // false2カウント
        }
    }

    inputFile.close();

    // 出力ファイルに結果を書き込み
    outputFile << "s,i,success,false,success2,false2\n";
    for (const auto &entry : results)
    {
        outputFile << entry.first.first << ","
                   << entry.first.second << ","
                   << std::get<0>(entry.second) << ","   // success
                   << std::get<1>(entry.second) << ","   // false
                   << std::get<2>(entry.second) << ","   // success2
                   << std::get<3>(entry.second) << "\n"; // false2
    }

    outputFile.close();

    std::cout << "Summary written to " << outputFilename << std::endl;

    return 0;
}
