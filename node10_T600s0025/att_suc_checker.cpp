#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <string>
#include <bitset>

std::vector<double> generateZipfDistribution(int n, double s)
{
    std::vector<double> distribution(n);
    double sum = 0.0;
    for (int i = 1; i <= n; ++i)
    {
        distribution[i - 1] = 1.0 / pow(i, s);
        sum += distribution[i - 1];
    }
    for (int i = 0; i < n; ++i)
    {
        distribution[i] /= sum;
    }
    return distribution;
}

int main()
{
    int n = 10;
    int decimalPoint = 1000;
    double delay = 5.303 * decimalPoint;
    double T = 600 * decimalPoint;

    std::string filename = "att_result/att_n" + std::to_string(n) + "_delay" + std::to_string(int(delay / decimalPoint)) + "_T" + std::to_string(int(T / decimalPoint)) + ".csv";
    std::ofstream file(filename);

    if (!file.is_open())
    {
        std::cerr << "ファイルを開くことができませんでした。" << std::endl;
        return 1;
    }

    file << "s,i,binary,staleRate,advMax,adv,success,success2\n";

    for (double s = 0.0; s <= 2.01; s += 0.025)
    { // <= を使用して 2.0 も含める
        std::vector<double> distribution = generateZipfDistribution(n, s);

        for (int i = 0; i < (1 << n); ++i)
        {
            double adv = 0.0;
            double sumRemaining = 0.0;
            double productSum = 0.0;
            int nodeCount = 0;

            std::vector<double> remainingElements;

            for (int j = 0; j < n; ++j)
            {
                if (i & (1 << j))
                {
                    adv += distribution[j];
                    nodeCount++;
                }
                else
                {
                    remainingElements.push_back(distribution[j]);
                    sumRemaining += distribution[j];
                }
            }

            // 残った要素の同士の積の和を計算 (全ての組み合わせを考慮)
            for (size_t m = 0; m < remainingElements.size(); ++m)
            {
                for (size_t n = 0; n < remainingElements.size(); ++n)
                {
                    if (m != n)
                    {
                        productSum += remainingElements[m] * remainingElements[n];
                    }
                }
            }

            double staleRate = sumRemaining != 0 ? delay * productSum / sumRemaining / T : 0;
            double advMax = sumRemaining / (1.0 + staleRate);
            int success = adv > advMax ? 1 : 0;
            int success2 = adv > (1 - adv) ? 1 : 0; // success2 を設定

            std::bitset<10> binaryRepresentation(i); // n=10 の場合
            file << std::fixed << std::setprecision(5) << s << "," << nodeCount << "," << binaryRepresentation << "," << staleRate << "," << advMax << "," << adv << "," << success << "," << success2 << "\n";
        }
    }

    file.close();
    std::cout << "計算が完了し、ファイルに保存されました: " << filename << std::endl;
    return 0;
}
