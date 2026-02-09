<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <script>
        function runTimer() {
            setTimeout(function() {
                location.reload();
            }, 600000); // 每10分鐘自動刷新
        }
    </script>
    <style>
        table {
            font-size: 22px;
            font-family: Arial, sans-serif;
            width: 500px;
            border: 1px solid black;
            border-collapse: collapse;
        }
        td {
            border: 1px solid black;
            padding: 8px;
        }
    </style>
</head>
<body onload="runTimer()">
<?php
ob_start();
header("Content-Type: text/html; charset=utf-8");
set_time_limit(0);
echo '<h1>存股-股價即時更新系統</h1>';
echo '<p>更新時間: ' . date("Y-m-d / H:i:s") . '</p>';
echo '<table>';
echo '<tr><td>股票名稱</td><td>股票代碼</td><td>即時股價</td><td>來源</td></tr>';

// 模擬瀏覽器抓取 HTML
function fetchStockPrice($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0');
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

// 從 Yahoo 擷取股價
function fetchYahooPrice($id) {
    $url = 'https://tw.stock.yahoo.com/quote/' . $id;
    $html = fetchStockPrice($url);
    $price = '-';

    if ($html) {
        $html_utf8 = mb_convert_encoding($html, 'UTF-8', 'auto');
        foreach (explode("\n", $html_utf8) as $line) {
            if (strpos($line, '<span class="Fz(32px) Fw(b) Lh(1) Mend(16px) ') !== false) {
                $replace_example00 = explode('<span class="Fz(32px) Fw(b) Lh(1) Mend(16px) ', $line);
                $replace_example01 = str_replace(array(">", "<"), '_', $replace_example00[1]);
                $replace_example02 = explode('_', $replace_example01);
                $price = htmlspecialchars($replace_example02[1]);
                break;
            }
        }
    }

    return $price;
}

// 從 CNYES 擷取股價（從 meta description）
function fetchCnyesPrice($id) {
    $url = 'https://www.cnyes.com/twstock/' . $id;
    $html = fetchStockPrice($url);
    $price = '-';

    if ($html) {
        $html_utf8 = mb_convert_encoding($html, 'UTF-8', 'auto');
        if (preg_match('/<meta name="description" content="[^"]*即時行情\s+([\d\.]+)/u', $html_utf8, $matches)) {
            $price = $matches[1];
        }
    }

    return $price;
}

// 指定要從 CNYES 查詢的股票名稱
$cnyesNames = array('皇家可口', '大東電', '悠遊卡', '台灣積層');

// 讀取 pandy.csv
$fp = fopen("/app/pandy.csv", "r");
$stockList = array();

if ($fp) {
    while (($data = fgetcsv($fp, 1000, ",", '"', '')) !== FALSE) {
        $name = trim($data[0]);
        $id = trim($data[1]);
        $price = '-';
        $source = 'Yahoo';

        if (in_array($name, $cnyesNames)) {
            $price = fetchCnyesPrice($id);
            $source = 'CNYES';
        } else {
            $price = fetchYahooPrice($id);
        }

        echo '<tr>';
        echo '<td>' . htmlspecialchars($name) . '</td>';
        echo '<td>' . htmlspecialchars($id) . '</td>';
        echo '<td>' . htmlspecialchars($price) . '</td>';
        echo '<td>' . $source . '</td>';
        echo '</tr>';

        $stockList[] = array(
            'name' => $name,
            'id' => $id,
            'price' => $price,
            'source' => $source,
            'time' => date("Y-m-d H:i:s")
        );
    }
    fclose($fp);
} else {
    echo '<tr><td colspan="4">❌ 無法開啟 pandy.csv 檔案。</td></tr>';
}
echo '</table>';

// 寫入 pandylist.csv
$fp_stocklist = fopen("/app/pandylist.csv", "w");
if ($fp_stocklist) {
    foreach ($stockList as $stock) {
        fputcsv($fp_stocklist, array(
            $stock['name'],
            $stock['id'],
            $stock['price'],
            $stock['source'],
            $stock['time']
        ), ',', '"', '', "\n");
    }
    fclose($fp_stocklist);
    echo '<p>✅ 已成功將資料寫入 pandylist.csv 檔案中。</p>';
} else {
    echo '<p>❌ 無法開啟 pandylist.csv 檔案進行寫入。</p>';
}
?>
<meta http-equiv="refresh" content="0;url=http://192.168.1.166/stock/pandytest.php" />
</body>
</html>
