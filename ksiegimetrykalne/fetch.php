<?php

function go_forest_deeper($data, $base_url){
//var_dump($data);
	$ret = array();
	foreach($data as $row){
		if(isset($row['folder']) && $row['folder'] === true){
			$next = isset($row['dir'])?$row['dir']:$row['title'];
			//$next = str_replace(array('Ś'), array('%C5%9A'), $next);
			$next = urlencode($next);
//echo "Enter: " . $next . "\n";
			$new_data = json_decode(file_get_contents($base_url . '/' . $next . '/index.json'), True);
			$r = go_forest_deeper($new_data, $base_url . '/' . $next);
			$ret = array_merge($ret, $r);
		} else {
			$ret[] = $base_url . '/' . $row['title'];
			echo $base_url . '/' . $row['title'] . "\n";
//echo "Get: " . $row['title'] . "\n";
		}
	}
	return $ret;
}

$data = json_decode(file_get_contents("index.json"), True);
$files = go_forest_deeper($data, 'https://img.ksiegimetrykalne.pl/file/ksiegimetrykalne');
foreach($files as $file){
	echo "$file\n";
}
