<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style>
        table {
            font-size: 22px;
            font-family: Arial;
            width: 500px;
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>存股-股價列表</h1>
    <p>更新時間: <?php echo date("Y-m-d / H:i:s"); ?></p>
    
    <!-- 新增下載連結 -->
    <p><a href="final.csv" download="final.csv">下載最終股票列表 (CSV)</a></p>
    <p><a href="stocklist.csv" download="stocklist.csv">下載最終股票列表 (CSV)</a></p>
    <table>
        <tr>
            <th>股票名稱</th>
            <th>價格</th>
        </tr>
        <?php
        // 檔案處理
        $input_file = "/app/stocklist.csv";
        $output_file = "/app/final.csv";
        
        // 打開輸出檔案以寫入 CSV，並確保編碼為 UTF-8
        $output = fopen($output_file, "w");
        
        // 寫入 UTF-8 BOM 以確保文件被識別為 UTF-8
        fwrite($output, chr(0xEF) . chr(0xBB) . chr(0xBF));
        
        // 寫入 CSV 標題
        fputcsv($output, ["股名", "股價"], ',', '"', '', "\n");
        
        // 打開輸入檔案以讀取 CSV
        $input = fopen($input_file, "r");
        
        // 讀取輸入檔案內容並寫入到輸出檔案
        while (($data = fgetcsv($input, 1000, ",", '"', '')) !== FALSE) {
            // 顯示表格內容
            echo "<tr>";
            echo "<td>" . $data[0] . "</td>";
            echo "<td>" . $data[2] . "</td>";
            echo "</tr>";
            
            // 寫入到 CSV
            fputcsv($output, [$data[0], $data[2]], ',', '"', '', "\n");
        }
        
        // 關閉檔案
        fclose($input);
        fclose($output);
        ?>
        <meta http-equiv="refresh" content="0;url=http://192.168.1.166/stock/pandylist.php" />
    </table>
</body>
</html>