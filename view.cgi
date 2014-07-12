#!/bin/bash

############################################################
# svn logから特定のキーワードが含まれるcommitを取得し
# commit情報を返す
############################################################

echo "Content-type:text/plain"
echo

########################################
# Settings
########################################
CMD_SVN="/usr/bin/svn";
CMD_XML_PARSE="/usr/bin/xmlstarlet sel -t";

SVN_USER="";
SVN_PASSWORD="";
SVN_OPTIONS=" --username ${SVN_USER} --password ${SVN_PASSWORD} --non-interactive --no-auth-cache --xml -r";
PARAM_KEYWORD="keyword";

########################################
# パラメータ取得
########################################
# 区切り文字を設定
tmpIFS=$IFS
IFS='=&'
parapara=($QUERY_STRING)
IFS=$tmpIFS
# parameterを格納し、keywordを取得
declare -a query_string_array
for ((i=0; i<${#parapara[@]}; i+=))
do
	query_string_array[${parapara[i]}]=${parapara[i+1]}
done
key_word=${query_string_array[${PARAM_KEYWORD}]};

########################################
# svnのlogからキーワードに紐づくリビジョンを取得する
########################################
declare -a revision_list=();
for rev in `$CMD_SVN log $SVN_OPTIONS 1:HEAD | $CMD_XML_PARSE -m "//logentry[contains(msg,'$key_word')]" -v "@revision" -n `
do
	revision_list+=($rev)
done

########################################
# revisionからファイルを取得とA / M / Dのステータスを取得
########################################
for rev in ${revision_list[@]};
	do
	# 指定revisionからxpathでステータス、ファイル名を抜出す
	for file_info_str in `$CMD_SVN log $SVN_OPTIONS $rev -v | $CMD_XML_PARSE -m "//logentry/paths/path" -v "concat(@action,',',text())" -n `
	do
		declare -a file_list=();
		# 「rev, 修正区分, ファイル名」で出力。形式はCSV
		echo $rev,$file_info_str,$((rev - 1));
	done
done

exit 0;

