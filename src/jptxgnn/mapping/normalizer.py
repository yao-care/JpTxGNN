"""主成分名稱標準化"""

import re
from typing import List, Tuple


# 日本語（カタカナ）→ 英語 薬物名対照表
# 一般的な医薬品約200種
JAPANESE_DRUG_DICT = {
    # === 解熱鎮痛薬 ===
    "アセトアミノフェン": "ACETAMINOPHEN",
    "アスピリン": "ASPIRIN",
    "イブプロフェン": "IBUPROFEN",
    "ロキソプロフェン": "LOXOPROFEN",
    "ジクロフェナク": "DICLOFENAC",
    "インドメタシン": "INDOMETHACIN",
    "ナプロキセン": "NAPROXEN",
    "セレコキシブ": "CELECOXIB",
    "メロキシカム": "MELOXICAM",
    "ピロキシカム": "PIROXICAM",

    # === 消化器系 ===
    "ファモチジン": "FAMOTIDINE",
    "ラニチジン": "RANITIDINE",
    "オメプラゾール": "OMEPRAZOLE",
    "ランソプラゾール": "LANSOPRAZOLE",
    "エソメプラゾール": "ESOMEPRAZOLE",
    "ラベプラゾール": "RABEPRAZOLE",
    "メトクロプラミド": "METOCLOPRAMIDE",
    "ドンペリドン": "DOMPERIDONE",
    "スクラルファート": "SUCRALFATE",
    "ミソプロストール": "MISOPROSTOL",

    # === 循環器系 ===
    "アムロジピン": "AMLODIPINE",
    "ニフェジピン": "NIFEDIPINE",
    "ベラパミル": "VERAPAMIL",
    "ジルチアゼム": "DILTIAZEM",
    "アテノロール": "ATENOLOL",
    "メトプロロール": "METOPROLOL",
    "プロプラノロール": "PROPRANOLOL",
    "カルベジロール": "CARVEDILOL",
    "ビソプロロール": "BISOPROLOL",
    "エナラプリル": "ENALAPRIL",
    "リシノプリル": "LISINOPRIL",
    "ロサルタン": "LOSARTAN",
    "バルサルタン": "VALSARTAN",
    "カンデサルタン": "CANDESARTAN",
    "テルミサルタン": "TELMISARTAN",
    "フロセミド": "FUROSEMIDE",
    "スピロノラクトン": "SPIRONOLACTONE",
    "ヒドロクロロチアジド": "HYDROCHLOROTHIAZIDE",
    "ワルファリン": "WARFARIN",
    "アスピリン": "ASPIRIN",
    "クロピドグレル": "CLOPIDOGREL",

    # === 糖尿病薬 ===
    "メトホルミン": "METFORMIN",
    "グリベンクラミド": "GLYBURIDE",
    "グリクラジド": "GLICLAZIDE",
    "グリメピリド": "GLIMEPIRIDE",
    "ピオグリタゾン": "PIOGLITAZONE",
    "シタグリプチン": "SITAGLIPTIN",
    "リナグリプチン": "LINAGLIPTIN",
    "エンパグリフロジン": "EMPAGLIFLOZIN",
    "ダパグリフロジン": "DAPAGLIFLOZIN",
    "インスリン": "INSULIN",

    # === 抗生物質 ===
    "アモキシシリン": "AMOXICILLIN",
    "アンピシリン": "AMPICILLIN",
    "セファレキシン": "CEPHALEXIN",
    "セフトリアキソン": "CEFTRIAXONE",
    "セフェピム": "CEFEPIME",
    "アジスロマイシン": "AZITHROMYCIN",
    "クラリスロマイシン": "CLARITHROMYCIN",
    "エリスロマイシン": "ERYTHROMYCIN",
    "レボフロキサシン": "LEVOFLOXACIN",
    "シプロフロキサシン": "CIPROFLOXACIN",
    "モキシフロキサシン": "MOXIFLOXACIN",
    "メトロニダゾール": "METRONIDAZOLE",
    "バンコマイシン": "VANCOMYCIN",
    "ゲンタマイシン": "GENTAMICIN",
    "ドキシサイクリン": "DOXYCYCLINE",
    "テトラサイクリン": "TETRACYCLINE",

    # === 抗真菌薬 ===
    "フルコナゾール": "FLUCONAZOLE",
    "イトラコナゾール": "ITRACONAZOLE",
    "ボリコナゾール": "VORICONAZOLE",
    "ナイスタチン": "NYSTATIN",
    "ミコナゾール": "MICONAZOLE",
    "クロトリマゾール": "CLOTRIMAZOLE",
    "テルビナフィン": "TERBINAFINE",

    # === 抗ウイルス薬 ===
    "アシクロビル": "ACYCLOVIR",
    "バラシクロビル": "VALACYCLOVIR",
    "オセルタミビル": "OSELTAMIVIR",
    "ザナミビル": "ZANAMIVIR",
    "リバビリン": "RIBAVIRIN",
    "ラミブジン": "LAMIVUDINE",
    "テノホビル": "TENOFOVIR",

    # === 精神神経系 ===
    "ジアゼパム": "DIAZEPAM",
    "ロラゼパム": "LORAZEPAM",
    "アルプラゾラム": "ALPRAZOLAM",
    "クロナゼパム": "CLONAZEPAM",
    "ゾルピデム": "ZOLPIDEM",
    "エスゾピクロン": "ESZOPICLONE",
    "フルオキセチン": "FLUOXETINE",
    "セルトラリン": "SERTRALINE",
    "パロキセチン": "PAROXETINE",
    "エスシタロプラム": "ESCITALOPRAM",
    "ベンラファキシン": "VENLAFAXINE",
    "デュロキセチン": "DULOXETINE",
    "ミルタザピン": "MIRTAZAPINE",
    "アミトリプチリン": "AMITRIPTYLINE",
    "ノルトリプチリン": "NORTRIPTYLINE",
    "リスペリドン": "RISPERIDONE",
    "オランザピン": "OLANZAPINE",
    "クエチアピン": "QUETIAPINE",
    "アリピプラゾール": "ARIPIPRAZOLE",
    "ハロペリドール": "HALOPERIDOL",
    "リチウム": "LITHIUM",
    "バルプロ酸": "VALPROIC ACID",
    "カルバマゼピン": "CARBAMAZEPINE",
    "フェニトイン": "PHENYTOIN",
    "レベチラセタム": "LEVETIRACETAM",
    "ラモトリギン": "LAMOTRIGINE",
    "トピラマート": "TOPIRAMATE",
    "ガバペンチン": "GABAPENTIN",
    "プレガバリン": "PREGABALIN",

    # === 呼吸器系 ===
    "サルブタモール": "ALBUTEROL",
    "サルメテロール": "SALMETEROL",
    "フォルモテロール": "FORMOTEROL",
    "フルチカゾン": "FLUTICASONE",
    "ブデソニド": "BUDESONIDE",
    "ベクロメタゾン": "BECLOMETHASONE",
    "モンテルカスト": "MONTELUKAST",
    "テオフィリン": "THEOPHYLLINE",
    "デキストロメトルファン": "DEXTROMETHORPHAN",
    "コデイン": "CODEINE",

    # === アレルギー・抗ヒスタミン ===
    "セチリジン": "CETIRIZINE",
    "ロラタジン": "LORATADINE",
    "フェキソフェナジン": "FEXOFENADINE",
    "デスロラタジン": "DESLORATADINE",
    "ジフェンヒドラミン": "DIPHENHYDRAMINE",
    "クロルフェニラミン": "CHLORPHENIRAMINE",
    "プロメタジン": "PROMETHAZINE",

    # === ステロイド ===
    "プレドニゾロン": "PREDNISOLONE",
    "プレドニゾン": "PREDNISONE",
    "メチルプレドニゾロン": "METHYLPREDNISOLONE",
    "デキサメタゾン": "DEXAMETHASONE",
    "ヒドロコルチゾン": "HYDROCORTISONE",
    "ベタメタゾン": "BETAMETHASONE",
    "トリアムシノロン": "TRIAMCINOLONE",

    # === 消化管運動・制吐薬 ===
    "オンダンセトロン": "ONDANSETRON",
    "グラニセトロン": "GRANISETRON",
    "プロクロルペラジン": "PROCHLORPERAZINE",
    "ロペラミド": "LOPERAMIDE",
    "センノシド": "SENNOSIDES",
    "ラクツロース": "LACTULOSE",
    "ビサコジル": "BISACODYL",

    # === 泌尿器系 ===
    "タムスロシン": "TAMSULOSIN",
    "シロドシン": "SILODOSIN",
    "フィナステリド": "FINASTERIDE",
    "デュタステリド": "DUTASTERIDE",
    "オキシブチニン": "OXYBUTYNIN",
    "ソリフェナシン": "SOLIFENACIN",
    "シルデナフィル": "SILDENAFIL",
    "タダラフィル": "TADALAFIL",

    # === 甲状腺 ===
    "レボチロキシン": "LEVOTHYROXINE",
    "メチマゾール": "METHIMAZOLE",
    "プロピルチオウラシル": "PROPYLTHIOURACIL",

    # === 骨粗鬆症 ===
    "アレンドロネート": "ALENDRONATE",
    "リセドロネート": "RISEDRONATE",
    "ゾレドロン酸": "ZOLEDRONIC ACID",
    "デノスマブ": "DENOSUMAB",
    "カルシトニン": "CALCITONIN",

    # === 高脂血症 ===
    "アトルバスタチン": "ATORVASTATIN",
    "ロスバスタチン": "ROSUVASTATIN",
    "シンバスタチン": "SIMVASTATIN",
    "プラバスタチン": "PRAVASTATIN",
    "フェノフィブラート": "FENOFIBRATE",
    "エゼチミブ": "EZETIMIBE",

    # === 痛風・高尿酸血症 ===
    "アロプリノール": "ALLOPURINOL",
    "フェブキソスタット": "FEBUXOSTAT",
    "コルヒチン": "COLCHICINE",

    # === 抗凝固薬・抗血栓薬 ===
    "ヘパリン": "HEPARIN",
    "エノキサパリン": "ENOXAPARIN",
    "ダビガトラン": "DABIGATRAN",
    "リバーロキサバン": "RIVAROXABAN",
    "アピキサバン": "APIXABAN",
    "エドキサバン": "EDOXABAN",
    "チクロピジン": "TICLOPIDINE",
    "プラスグレル": "PRASUGREL",

    # === 免疫抑制薬 ===
    "タクロリムス": "TACROLIMUS",
    "シクロスポリン": "CYCLOSPORINE",
    "アザチオプリン": "AZATHIOPRINE",
    "ミコフェノール酸": "MYCOPHENOLIC ACID",
    "メトトレキサート": "METHOTREXATE",
    "シクロホスファミド": "CYCLOPHOSPHAMIDE",

    # === 抗癌剤（一部） ===
    "パクリタキセル": "PACLITAXEL",
    "ドセタキセル": "DOCETAXEL",
    "シスプラチン": "CISPLATIN",
    "カルボプラチン": "CARBOPLATIN",
    "フルオロウラシル": "FLUOROURACIL",
    "カペシタビン": "CAPECITABINE",
    "ゲムシタビン": "GEMCITABINE",
    "ドキソルビシン": "DOXORUBICIN",
    "イマチニブ": "IMATINIB",
    "エルロチニブ": "ERLOTINIB",
    "ゲフィチニブ": "GEFITINIB",

    # === 局所麻酔・麻酔補助 ===
    "リドカイン": "LIDOCAINE",
    "プロカイン": "PROCAINE",
    "ブピバカイン": "BUPIVACAINE",
    "ロピバカイン": "ROPIVACAINE",
    "プロポフォール": "PROPOFOL",
    "ケタミン": "KETAMINE",
    "フェンタニル": "FENTANYL",
    "モルヒネ": "MORPHINE",
    "オキシコドン": "OXYCODONE",
    "トラマドール": "TRAMADOL",

    # === ビタミン・ミネラル ===
    "ビタミンＢ１": "THIAMINE",
    "チアミン": "THIAMINE",
    "ビタミンＢ２": "RIBOFLAVIN",
    "リボフラビン": "RIBOFLAVIN",
    "ビタミンＢ６": "PYRIDOXINE",
    "ピリドキシン": "PYRIDOXINE",
    "ビタミンＢ１２": "CYANOCOBALAMIN",
    "シアノコバラミン": "CYANOCOBALAMIN",
    "ビタミンＣ": "ASCORBIC ACID",
    "アスコルビン酸": "ASCORBIC ACID",
    "ビタミンＤ": "CHOLECALCIFEROL",
    "コレカルシフェロール": "CHOLECALCIFEROL",
    "ビタミンＥ": "TOCOPHEROL",
    "トコフェロール": "TOCOPHEROL",
    "ビタミンＫ": "PHYTONADIONE",
    "フィトナジオン": "PHYTONADIONE",
    "葉酸": "FOLIC ACID",
    "カルシウム": "CALCIUM",
    "マグネシウム": "MAGNESIUM",
    "亜鉛": "ZINC",
    "鉄": "IRON",

    # === 眼科 ===
    "チモロール": "TIMOLOL",
    "ラタノプロスト": "LATANOPROST",
    "ピロカルピン": "PILOCARPINE",
    "アトロピン": "ATROPINE",
    "トロピカミド": "TROPICAMIDE",

    # === 追加: 未マッピング薬物（PMDA データより）===
    # 解熱鎮痛薬・抗炎症薬
    "エトドラク": "ETODOLAC",
    "ケトプロフェン": "KETOPROFEN",
    "フルルビプロフェン": "FLURBIPROFEN",
    "オキサプロジン": "OXAPROZIN",
    "チアプロフェン酸": "TIAPROFENIC ACID",
    "スリンダク": "SULINDAC",
    "ナブメトン": "NABUMETONE",
    "エトリコキシブ": "ETORICOXIB",

    # 糖尿病薬
    "ボグリボース": "VOGLIBOSE",
    "アカルボース": "ACARBOSE",
    "ミグリトール": "MIGLITOL",
    "ナテグリニド": "NATEGLINIDE",
    "レパグリニド": "REPAGLINIDE",
    "ミチグリニド": "MITIGLINIDE",
    "ビルダグリプチン": "VILDAGLIPTIN",
    "アログリプチン": "ALOGLIPTIN",
    "テネリグリプチン": "TENELIGLIPTIN",
    "アナグリプチン": "ANAGLIPTIN",
    "サキサグリプチン": "SAXAGLIPTIN",
    "トホグリフロジン": "TOFOGLIFLOZIN",
    "イプラグリフロジン": "IPRAGLIFLOZIN",
    "ルセオグリフロジン": "LUSEOGLIFLOZIN",
    "カナグリフロジン": "CANAGLIFLOZIN",

    # パーキンソン病
    "ペルゴリド": "PERGOLIDE",
    "プラミペキソール": "PRAMIPEXOLE",
    "ロピニロール": "ROPINIROLE",
    "ロチゴチン": "ROTIGOTINE",
    "セレギリン": "SELEGILINE",
    "ラサギリン": "RASAGILINE",
    "エンタカポン": "ENTACAPONE",
    "トリヘキシフェニジル": "TRIHEXYPHENIDYL",
    "ビペリデン": "BIPERIDEN",
    "アマンタジン": "AMANTADINE",
    "レボドパ": "LEVODOPA",
    "カルビドパ": "CARBIDOPA",
    "ドロキシドパ": "DROXIDOPA",

    # カルシウム拮抗薬
    "フェロジピン": "FELODIPINE",
    "シルニジピン": "CILNIDIPINE",
    "ニカルジピン": "NICARDIPINE",
    "ニルバジピン": "NILVADIPINE",
    "ニソルジピン": "NISOLDIPINE",
    "ニトレンジピン": "NITRENDIPINE",
    "バルニジピン": "BARNIDIPINE",
    "エホニジピン": "EFONIDIPINE",
    "アゼルニジピン": "AZELNIDIPINE",
    "ベニジピン": "BENIDIPINE",
    "マニジピン": "MANIDIPINE",

    # 高脂血症薬
    "ベザフィブラート": "BEZAFIBRATE",
    "クロフィブラート": "CLOFIBRATE",
    "ペマフィブラート": "PEMAFIBRATE",
    "ピタバスタチン": "PITAVASTATIN",
    "フルバスタチン": "FLUVASTATIN",
    "コレスチラミン": "CHOLESTYRAMINE",
    "コレスチポール": "COLESTIPOL",
    "コレスチミド": "COLESTIMIDE",
    "プロブコール": "PROBUCOL",

    # 消化器系
    "イトプリド": "ITOPRIDE",
    "モサプリド": "MOSAPRIDE",
    "トリメブチン": "TRIMEBUTINE",
    "ポラプレジンク": "POLAPREZINC",
    "テプレノン": "TEPRENONE",
    "レバミピド": "REBAMIPIDE",
    "イルソグラジン": "IRSOGLADINE",
    "ボノプラザン": "VONOPRAZAN",
    "タケプロン": "LANSOPRAZOLE",
    "ネキシウム": "ESOMEPRAZOLE",

    # 抗癌剤
    "トレミフェン": "TOREMIFENE",
    "タモキシフェン": "TAMOXIFEN",
    "アナストロゾール": "ANASTROZOLE",
    "レトロゾール": "LETROZOLE",
    "エキセメスタン": "EXEMESTANE",
    "フルタミド": "FLUTAMIDE",
    "ビカルタミド": "BICALUTAMIDE",
    "エンザルタミド": "ENZALUTAMIDE",
    "アビラテロン": "ABIRATERONE",
    "ソラフェニブ": "SORAFENIB",
    "スニチニブ": "SUNITINIB",
    "パゾパニブ": "PAZOPANIB",
    "レゴラフェニブ": "REGORAFENIB",
    "レンバチニブ": "LENVATINIB",
    "アキシチニブ": "AXITINIB",
    "カボザンチニブ": "CABOZANTINIB",
    "オシメルチニブ": "OSIMERTINIB",
    "アファチニブ": "AFATINIB",
    "ダコミチニブ": "DACOMITINIB",
    "クリゾチニブ": "CRIZOTINIB",
    "アレクチニブ": "ALECTINIB",
    "セリチニブ": "CERITINIB",
    "ロルラチニブ": "LORLATINIB",
    "ダブラフェニブ": "DABRAFENIB",
    "トラメチニブ": "TRAMETINIB",
    "ベムラフェニブ": "VEMURAFENIB",
    "イブルチニブ": "IBRUTINIB",
    "アカラブルチニブ": "ACALABRUTINIB",
    "ベネトクラクス": "VENETOCLAX",
    "ポマリドミド": "POMALIDOMIDE",
    "レナリドミド": "LENALIDOMIDE",
    "サリドマイド": "THALIDOMIDE",
    "ボルテゾミブ": "BORTEZOMIB",
    "カルフィルゾミブ": "CARFILZOMIB",
    "イキサゾミブ": "IXAZOMIB",

    # ビタミン・栄養素
    "メナテトレノン": "MENATETRENONE",
    "トコフェロールニコチン酸エステル": "TOCOPHEROL NICOTINATE",
    "メコバラミン": "MECOBALAMIN",
    "ベンフォチアミン": "BENFOTIAMINE",
    "フルスルチアミン": "FURSULTIAMINE",
    "パンテチン": "PANTETHINE",
    "カルニチン": "CARNITINE",
    "ユビデカレノン": "UBIDECARENONE",
    "コエンザイムキューテン": "UBIQUINONE",

    # 抗不整脈薬
    "ピルシカイニド": "PILSICAINIDE",
    "シベンゾリン": "CIBENZOLINE",
    "プロパフェノン": "PROPAFENONE",
    "フレカイニド": "FLECAINIDE",
    "ジソピラミド": "DISOPYRAMIDE",
    "キニジン": "QUINIDINE",
    "プロカインアミド": "PROCAINAMIDE",
    "メキシレチン": "MEXILETINE",
    "アプリンジン": "APRINDINE",
    "ソタロール": "SOTALOL",
    "アミオダロン": "AMIODARONE",
    "ニフェカラント": "NIFEKALANT",
    "ベプリジル": "BEPRIDIL",

    # 抗血栓薬
    "シロスタゾール": "CILOSTAZOL",
    "サルポグレラート": "SARPOGRELATE",
    "ベラプロスト": "BERAPROST",
    "リマプロスト": "LIMAPROST",

    # 泌尿器系
    "ナフトピジル": "NAFTOPIDIL",
    "プロピベリン": "PROPIVERINE",
    "イミダフェナシン": "IMIDAFENACIN",
    "トルテロジン": "TOLTERODINE",
    "フェソテロジン": "FESOTERODINE",
    "ミラベグロン": "MIRABEGRON",
    "ビベグロン": "VIBEGRON",

    # 皮膚科
    "タクロリムス": "TACROLIMUS",
    "ピメクロリムス": "PIMECROLIMUS",
    "アダパレン": "ADAPALENE",
    "トレチノイン": "TRETINOIN",
    "イソトレチノイン": "ISOTRETINOIN",
    "カルシポトリオール": "CALCIPOTRIOL",
    "タカルシトール": "TACALCITOL",
    "マキサカルシトール": "MAXACALCITOL",

    # 抗アレルギー薬
    "オロパタジン": "OLOPATADINE",
    "エピナスチン": "EPINASTINE",
    "ベポタスチン": "BEPOTASTINE",
    "エバスチン": "EBASTINE",
    "レボセチリジン": "LEVOCETIRIZINE",
    "ビラスチン": "BILASTINE",
    "ルパタジン": "RUPATADINE",
    "クロモグリク酸": "CROMOGLICIC ACID",
    "ペミロラスト": "PEMIROLAST",
    "トラニラスト": "TRANILAST",
    "ケトチフェン": "KETOTIFEN",
    "アゼラスチン": "AZELASTINE",
    "オザグレル": "OZAGREL",
    "プランルカスト": "PRANLUKAST",
    "ザフィルルカスト": "ZAFIRLUKAST",

    # 免疫調整薬
    "レフルノミド": "LEFLUNOMIDE",
    "イグラチモド": "IGURATIMOD",
    "サラゾスルファピリジン": "SULFASALAZINE",
    "ブシラミン": "BUCILLAMINE",
    "ペニシラミン": "PENICILLAMINE",
    "オーラノフィン": "AURANOFIN",
    "エタネルセプト": "ETANERCEPT",
    "アダリムマブ": "ADALIMUMAB",
    "インフリキシマブ": "INFLIXIMAB",
    "ゴリムマブ": "GOLIMUMAB",
    "セルトリズマブ": "CERTOLIZUMAB",
    "トシリズマブ": "TOCILIZUMAB",
    "サリルマブ": "SARILUMAB",
    "アバタセプト": "ABATACEPT",
    "トファシチニブ": "TOFACITINIB",
    "バリシチニブ": "BARICITINIB",
    "ウパダシチニブ": "UPADACITINIB",
    "フィルゴチニブ": "FILGOTINIB",
    "ペフィシチニブ": "PEFICITINIB",
    "リツキシマブ": "RITUXIMAB",

    # 筋弛緩薬
    "エペリゾン": "EPERISONE",
    "チザニジン": "TIZANIDINE",
    "バクロフェン": "BACLOFEN",
    "ダントロレン": "DANTROLENE",
    "アフロクアロン": "AFLOQUALONE",
    "クロルフェネシン": "CHLORPHENESIN",

    # 抗めまい薬
    "ベタヒスチン": "BETAHISTINE",
    "ジフェニドール": "DIPHENIDOL",

    # 甲状腺
    "チアマゾール": "THIAMAZOLE",
    "ヨウ化カリウム": "POTASSIUM IODIDE",

    # 抗てんかん薬
    "ペランパネル": "PERAMPANEL",
    "ラコサミド": "LACOSAMIDE",
    "ルフィナミド": "RUFINAMIDE",
    "スチリペントール": "STIRIPENTOL",
    "クロバザム": "CLOBAZAM",
    "エトスクシミド": "ETHOSUXIMIDE",
    "ゾニサミド": "ZONISAMIDE",
    "フェノバルビタール": "PHENOBARBITAL",
    "プリミドン": "PRIMIDONE",

    # 認知症薬
    "ドネペジル": "DONEPEZIL",
    "ガランタミン": "GALANTAMINE",
    "リバスチグミン": "RIVASTIGMINE",
    "メマンチン": "MEMANTINE",

    # その他
    "イコサペント酸エチル": "ICOSAPENT ETHYL",
    "オメガスリー脂肪酸": "OMEGA-3 FATTY ACIDS",

    # ===== 日本の商品名 → 一般名 マッピング =====
    # 消化器系
    "ムコダイン": "CARBOCISTEINE",
    "カイトリル": "GRANISETRON",
    "ナウゼリン": "DOMPERIDONE",
    "プリンペラン": "METOCLOPRAMIDE",
    "ガスター": "FAMOTIDINE",
    "タケプロン": "LANSOPRAZOLE",
    "ネキシウム": "ESOMEPRAZOLE",
    "パリエット": "RABEPRAZOLE",
    "タケキャブ": "VONOPRAZAN",
    "ガスモチン": "MOSAPRIDE",
    "セレキノン": "TRIMEBUTINE",
    "コロネル": "POLYCARBOPHIL",
    "ビオフェルミン": "LACTOBACILLUS",
    "ブスコパン": "BUTYLSCOPOLAMINE",
    "ストロカイン": "OXETHAZAINE",
    "マーロックス": "MAGALDRATE",

    # 鎮痛・抗炎症
    "ボルタレン": "DICLOFENAC",
    "ロキソニン": "LOXOPROFEN",
    "セレコックス": "CELECOXIB",
    "カロナール": "ACETAMINOPHEN",
    "ブルフェン": "IBUPROFEN",
    "インダシン": "INDOMETHACIN",
    "モービック": "MELOXICAM",
    "ハイペン": "ETODOLAC",
    "ロルカム": "LORNOXICAM",
    "ソレトン": "ZALTOPROFEN",
    "インフリー": "AMPIROXICAM",

    # 循環器系
    "アムロジン": "AMLODIPINE",
    "ノルバスク": "AMLODIPINE",
    "アダラート": "NIFEDIPINE",
    "ヘルベッサー": "DILTIAZEM",
    "ワソラン": "VERAPAMIL",
    "メインテート": "BISOPROLOL",
    "テノーミン": "ATENOLOL",
    "インデラル": "PROPRANOLOL",
    "ラシックス": "FUROSEMIDE",
    "アルダクトン": "SPIRONOLACTONE",
    "フルイトラン": "TRICHLORMETHIAZIDE",
    "ディオバン": "VALSARTAN",
    "ブロプレス": "CANDESARTAN",
    "ミカルディス": "TELMISARTAN",
    "オルメテック": "OLMESARTAN",
    "アジルバ": "AZILSARTAN",
    "レニベース": "ENALAPRIL",
    "プラビックス": "CLOPIDOGREL",
    "バイアスピリン": "ASPIRIN",
    "ワーファリン": "WARFARIN",
    "プレタール": "CILOSTAZOL",
    "エパデール": "ICOSAPENT ETHYL",
    "ロトリガ": "OMEGA-3 FATTY ACIDS",
    "リバロ": "PITAVASTATIN",
    "クレストール": "ROSUVASTATIN",
    "リピトール": "ATORVASTATIN",
    "メバロチン": "PRAVASTATIN",
    "リポバス": "SIMVASTATIN",
    "ゼチーア": "EZETIMIBE",
    "ベザトール": "BEZAFIBRATE",
    "トライコア": "FENOFIBRATE",
    "カルバン": "BEVANTOLOL",
    "デタントール": "BUNAZOSIN",

    # 精神神経系
    "デパス": "ETIZOLAM",
    "ソラナックス": "ALPRAZOLAM",
    "リーゼ": "CLOTIAZEPAM",
    "セルシン": "DIAZEPAM",
    "ワイパックス": "LORAZEPAM",
    "メイラックス": "LOFLAZEPATE",
    "レンドルミン": "BROTIZOLAM",
    "マイスリー": "ZOLPIDEM",
    "ルネスタ": "ESZOPICLONE",
    "ベルソムラ": "SUVOREXANT",
    "デエビゴ": "LEMBOREXANT",
    "ジェイゾロフト": "SERTRALINE",
    "パキシル": "PAROXETINE",
    "レクサプロ": "ESCITALOPRAM",
    "サインバルタ": "DULOXETINE",
    "イフェクサー": "VENLAFAXINE",
    "リフレックス": "MIRTAZAPINE",
    "レメロン": "MIRTAZAPINE",
    "トリプタノール": "AMITRIPTYLINE",
    "アナフラニール": "CLOMIPRAMINE",
    "リスパダール": "RISPERIDONE",
    "ジプレキサ": "OLANZAPINE",
    "セロクエル": "QUETIAPINE",
    "エビリファイ": "ARIPIPRAZOLE",
    "ロナセン": "BLONANSERIN",
    "ルーラン": "PEROSPIRONE",
    "セレネース": "HALOPERIDOL",
    "デパケン": "VALPROIC ACID",
    "テグレトール": "CARBAMAZEPINE",
    "アレビアチン": "PHENYTOIN",
    "リボトリール": "CLONAZEPAM",
    "ランドセン": "CLONAZEPAM",
    "イーケプラ": "LEVETIRACETAM",
    "ラミクタール": "LAMOTRIGINE",
    "トピナ": "TOPIRAMATE",
    "ガバペン": "GABAPENTIN",
    "リリカ": "PREGABALIN",
    "フィコンパ": "PERAMPANEL",
    "ビムパット": "LACOSAMIDE",
    "アリセプト": "DONEPEZIL",
    "レミニール": "GALANTAMINE",
    "イクセロン": "RIVASTIGMINE",
    "リバスタッチ": "RIVASTIGMINE",
    "メマリー": "MEMANTINE",

    # 呼吸器系
    "メプチン": "PROCATEROL",
    "ベネトリン": "SALBUTAMOL",
    "セレベント": "SALMETEROL",
    "シムビコート": "BUDESONIDE",
    "アドエア": "FLUTICASONE",
    "レルベア": "VILANTEROL",
    "スピリーバ": "TIOTROPIUM",
    "オンブレス": "INDACATEROL",
    "ウルティブロ": "GLYCOPYRRONIUM",
    "シングレア": "MONTELUKAST",
    "キプレス": "MONTELUKAST",
    "オノン": "PRANLUKAST",
    "テオドール": "THEOPHYLLINE",
    "ユニフィル": "THEOPHYLLINE",
    "アストミン": "DIMEMORFAN",
    "メジコン": "DEXTROMETHORPHAN",
    "アスベリン": "TIPEPIDINE",
    "ムコソルバン": "AMBROXOL",
    "ビソルボン": "BROMHEXINE",

    # 抗アレルギー
    "アレグラ": "FEXOFENADINE",
    "クラリチン": "LORATADINE",
    "ジルテック": "CETIRIZINE",
    "ザイザル": "LEVOCETIRIZINE",
    "アレジオン": "EPINASTINE",
    "アレロック": "OLOPATADINE",
    "タリオン": "BEPOTASTINE",
    "エバステル": "EBASTINE",
    "デザレックス": "DESLORATADINE",
    "ルパフィン": "RUPATADINE",
    "ビラノア": "BILASTINE",
    "ポララミン": "CHLORPHENIRAMINE",
    "レスタミン": "DIPHENHYDRAMINE",
    "ピレチア": "PROMETHAZINE",

    # 抗生物質
    "クラビット": "LEVOFLOXACIN",
    "シプロキサン": "CIPROFLOXACIN",
    "オゼックス": "TOSUFLOXACIN",
    "グレースビット": "SITAFLOXACIN",
    "アベロックス": "MOXIFLOXACIN",
    "クラリス": "CLARITHROMYCIN",
    "クラリシッド": "CLARITHROMYCIN",
    "ジスロマック": "AZITHROMYCIN",
    "エリスロシン": "ERYTHROMYCIN",
    "サワシリン": "AMOXICILLIN",
    "パセトシン": "AMOXICILLIN",
    "ビクシリン": "AMPICILLIN",
    "ケフレックス": "CEPHALEXIN",
    "フロモックス": "CEFCAPENE",
    "メイアクト": "CEFDITOREN",
    "セフゾン": "CEFDINIR",
    "バナン": "CEFPODOXIME",
    "ロセフィン": "CEFTRIAXONE",
    "モダシン": "CEFTAZIDIME",
    "チエナム": "IMIPENEM",
    "メロペン": "MEROPENEM",
    "バンコマイシン": "VANCOMYCIN",
    "ミノマイシン": "MINOCYCLINE",
    "ビブラマイシン": "DOXYCYCLINE",
    "ダラシン": "CLINDAMYCIN",
    "フラジール": "METRONIDAZOLE",
    "ファンギゾン": "AMPHOTERICIN B",
    "ジフルカン": "FLUCONAZOLE",
    "イトリゾール": "ITRACONAZOLE",
    "ブイフェンド": "VORICONAZOLE",

    # 糖尿病
    "メトグルコ": "METFORMIN",
    "グリミクロン": "GLICLAZIDE",
    "アマリール": "GLIMEPIRIDE",
    "オイグルコン": "GLYBURIDE",
    "アクトス": "PIOGLITAZONE",
    "ジャヌビア": "SITAGLIPTIN",
    "エクア": "VILDAGLIPTIN",
    "ネシーナ": "ALOGLIPTIN",
    "トラゼンタ": "LINAGLIPTIN",
    "テネリア": "TENELIGLIPTIN",
    "オングリザ": "SAXAGLIPTIN",
    "スーグラ": "IPRAGLIFLOZIN",
    "フォシーガ": "DAPAGLIFLOZIN",
    "ジャディアンス": "EMPAGLIFLOZIN",
    "カナグル": "CANAGLIFLOZIN",
    "デベルザ": "TOFOGLIFLOZIN",
    "ルセフィ": "LUSEOGLIFLOZIN",
    "ベイスン": "VOGLIBOSE",
    "グルコバイ": "ACARBOSE",
    "セイブル": "MIGLITOL",
    "ファスティック": "NATEGLINIDE",
    "スターシス": "NATEGLINIDE",
    "グルファスト": "MITIGLINIDE",
    "シュアポスト": "REPAGLINIDE",
    "ビクトーザ": "LIRAGLUTIDE",
    "トルリシティ": "DULAGLUTIDE",
    "オゼンピック": "SEMAGLUTIDE",
    "リベルサス": "SEMAGLUTIDE",
    "バイエッタ": "EXENATIDE",

    # 骨・関節
    "フォサマック": "ALENDRONATE",
    "ボナロン": "ALENDRONATE",
    "アクトネル": "RISEDRONATE",
    "ベネット": "RISEDRONATE",
    "リカルボン": "MINODRONATE",
    "ボノテオ": "MINODRONATE",
    "プラリア": "DENOSUMAB",
    "イベニティ": "ROMOSOZUMAB",
    "フォルテオ": "TERIPARATIDE",
    "テリボン": "TERIPARATIDE",
    "エディロール": "ELDECALCITOL",
    "アルファロール": "ALFACALCIDOL",
    "ワンアルファ": "ALFACALCIDOL",
    "ロコアテープ": "ESFLURBIPROFEN",
    "モーラステープ": "KETOPROFEN",
    "ボルタレンテープ": "DICLOFENAC",
    "ロキソニンテープ": "LOXOPROFEN",

    # 泌尿器
    "ハルナール": "TAMSULOSIN",
    "ユリーフ": "SILODOSIN",
    "フリバス": "NAFTOPIDIL",
    "アボルブ": "DUTASTERIDE",
    "プロスカー": "FINASTERIDE",
    "プロペシア": "FINASTERIDE",
    "ベタニス": "MIRABEGRON",
    "ベオーバ": "VIBEGRON",
    "ベシケア": "SOLIFENACIN",
    "ウリトス": "IMIDAFENACIN",
    "ステーブラ": "IMIDAFENACIN",
    "トビエース": "FESOTERODINE",
    "デトルシトール": "TOLTERODINE",
    "バップフォー": "PROPIVERINE",
    "バイアグラ": "SILDENAFIL",
    "シアリス": "TADALAFIL",
    "レビトラ": "VARDENAFIL",

    # 甲状腺
    "チラーヂン": "LEVOTHYROXINE",
    "メルカゾール": "THIAMAZOLE",
    "チウラジール": "PROPYLTHIOURACIL",

    # 痛風
    "ザイロリック": "ALLOPURINOL",
    "フェブリク": "FEBUXOSTAT",
    "トピロリック": "TOPIROXOSTAT",
    "ウリアデック": "TOPIROXOSTAT",
    "ユリノーム": "BENZBROMARONE",
    "コルヒチン": "COLCHICINE",

    # ステロイド
    "プレドニン": "PREDNISOLONE",
    "メドロール": "METHYLPREDNISOLONE",
    "デカドロン": "DEXAMETHASONE",
    "リンデロン": "BETAMETHASONE",
    "ケナコルト": "TRIAMCINOLONE",
    "コートリル": "HYDROCORTISONE",

    # 免疫抑制
    "プログラフ": "TACROLIMUS",
    "ネオーラル": "CYCLOSPORINE",
    "サンディミュン": "CYCLOSPORINE",
    "イムラン": "AZATHIOPRINE",
    "アザニン": "AZATHIOPRINE",
    "セルセプト": "MYCOPHENOLIC ACID",
    "ブレディニン": "MIZORIBINE",
    "リウマトレックス": "METHOTREXATE",
    "アラバ": "LEFLUNOMIDE",
    "オレンシア": "ABATACEPT",
    "ヒュミラ": "ADALIMUMAB",
    "レミケード": "INFLIXIMAB",
    "シンポニー": "GOLIMUMAB",
    "エンブレル": "ETANERCEPT",
    "アクテムラ": "TOCILIZUMAB",
    "コセンティクス": "SECUKINUMAB",
    "トルツ": "IXEKIZUMAB",
    "ステラーラ": "USTEKINUMAB",
    "ゼルヤンツ": "TOFACITINIB",
    "オルミエント": "BARICITINIB",
    "リンヴォック": "UPADACITINIB",
    "ジセレカ": "FILGOTINIB",
    "スマイラフ": "PEFICITINIB",
    "リツキサン": "RITUXIMAB",

    # パーキンソン病
    "ネオドパストン": "LEVODOPA",
    "マドパー": "LEVODOPA",
    "メネシット": "LEVODOPA",
    "スタレボ": "LEVODOPA",
    "パーロデル": "BROMOCRIPTINE",
    "カバサール": "CABERGOLINE",
    "ビ・シフロール": "PRAMIPEXOLE",
    "レキップ": "ROPINIROLE",
    "ニュープロパッチ": "ROTIGOTINE",
    "アジレクト": "RASAGILINE",
    "エフピー": "SELEGILINE",
    "コムタン": "ENTACAPONE",
    "オンジェンティス": "OPICAPONE",
    "エクフィナ": "SAFINAMIDE",
    "アーテン": "TRIHEXYPHENIDYL",
    "アキネトン": "BIPERIDEN",
    "シンメトレル": "AMANTADINE",
    "ドプス": "DROXIDOPA",
    "ノウリアスト": "ISTRADEFYLLINE",

    # 抗不整脈
    "サンリズム": "PILSICAINIDE",
    "シベノール": "CIBENZOLINE",
    "プロノン": "PROPAFENONE",
    "タンボコール": "FLECAINIDE",
    "リスモダン": "DISOPYRAMIDE",
    "キシロカイン": "LIDOCAINE",
    "メキシチール": "MEXILETINE",
    "アスペノン": "APRINDINE",
    "ソタコール": "SOTALOL",
    "アンカロン": "AMIODARONE",
    "シンビット": "NIFEKALANT",
    "ベプリコール": "BEPRIDIL",

    # 診断薬
    "バリトゲン": "BARIUM",
    "バリトップ": "BARIUM",
    "ガストログラフィン": "DIATRIZOATE",
    "オムニパーク": "IOHEXOL",
    "イオパミロン": "IOPAMIDOL",
    "オプチレイ": "IOVERSOL",

    # 筋弛緩
    "テルネリン": "TIZANIDINE",
    "ミオナール": "EPERISONE",
    "ギャバロン": "BACLOFEN",
    "ダントリウム": "DANTROLENE",
    "アロフト": "AFLOQUALONE",

    # 抗てんかん（追加）
    "ラクサミド": "LACOSAMIDE",
    "エクセグラン": "ZONISAMIDE",
    "マイスタン": "CLOBAZAM",
    "ザロンチン": "ETHOSUXIMIDE",
    "フェノバール": "PHENOBARBITAL",

    # 眼科
    "キサラタン": "LATANOPROST",
    "トラバタンズ": "TRAVOPROST",
    "ルミガン": "BIMATOPROST",
    "タプロス": "TAFLUPROST",
    "チモプトール": "TIMOLOL",
    "ミケラン": "CARTEOLOL",
    "トルソプト": "DORZOLAMIDE",
    "エイゾプト": "BRINZOLAMIDE",
    "アイファガン": "BRIMONIDINE",
    "ミドリン": "TROPICAMIDE",
    "サンドール": "PHENYLEPHRINE",
    "ミドリンＰ": "TROPICAMIDE",
    "ネオシネジン": "PHENYLEPHRINE",
    "パタノール": "OLOPATADINE",
    "アレジオン": "EPINASTINE",
    "リボスチン": "LEVOCABASTINE",
    "クラビット点眼": "LEVOFLOXACIN",
    "ガチフロ点眼": "GATIFLOXACIN",
    "ベガモックス": "MOXIFLOXACIN",
    "フルメトロン": "FLUOROMETHOLONE",
    "リンデロン点眼": "BETAMETHASONE",

    # 皮膚科
    "アンテベート": "BETAMETHASONE",
    "マイザー": "DIFLUPREDNATE",
    "デルモベート": "CLOBETASOL",
    "ネリゾナ": "DIFLUCORTOLONE",
    "フルコート": "FLUOCINOLONE",
    "ロコイド": "HYDROCORTISONE",
    "キンダベート": "CLOBETASONE",
    "プロトピック": "TACROLIMUS",
    "エリデル": "PIMECROLIMUS",
    "ディフェリン": "ADAPALENE",
    "ベピオ": "BENZOYL PEROXIDE",
    "エピデュオ": "ADAPALENE",
    "ドボベット": "CALCIPOTRIOL",
    "ボンアルファ": "TACALCITOL",
    "オキサロール": "MAXACALCITOL",
    "ゲンタシン": "GENTAMICIN",
    "フシジン": "FUSIDIC ACID",
    "アクアチム": "NADIFLOXACIN",
    "ゼビアックス": "OZENOXACIN",
    "ラミシール": "TERBINAFINE",
    "ルリコン": "LULICONAZOLE",
    "ニゾラール": "KETOCONAZOLE",
    "アスタット": "LANOCONAZOLE",

    # 抗癌剤商品名
    "オプジーボ": "NIVOLUMAB",
    "キイトルーダ": "PEMBROLIZUMAB",
    "テセントリク": "ATEZOLIZUMAB",
    "イミフィンジ": "DURVALUMAB",
    "ヤーボイ": "IPILIMUMAB",
    "ハーセプチン": "TRASTUZUMAB",
    "パージェタ": "PERTUZUMAB",
    "アバスチン": "BEVACIZUMAB",
    "アービタックス": "CETUXIMAB",
    "ベクティビックス": "PANITUMUMAB",
    "タルセバ": "ERLOTINIB",
    "イレッサ": "GEFITINIB",
    "タグリッソ": "OSIMERTINIB",
    "ジオトリフ": "AFATINIB",
    "グリベック": "IMATINIB",
    "スプリセル": "DASATINIB",
    "タシグナ": "NILOTINIB",
    "ボシュリフ": "BOSUTINIB",
    "アイクルシグ": "PONATINIB",
    "ザーコリ": "CRIZOTINIB",
    "アレセンサ": "ALECTINIB",
    "ジカディア": "CERITINIB",
    "ローブレナ": "LORLATINIB",
    "タフィンラー": "DABRAFENIB",
    "メキニスト": "TRAMETINIB",
    "ゼルボラフ": "VEMURAFENIB",
    "イムブルビカ": "IBRUTINIB",
    "カルケンス": "ACALABRUTINIB",
    "ベネクレクスタ": "VENETOCLAX",
    "レブラミド": "LENALIDOMIDE",
    "ポマリスト": "POMALIDOMIDE",
    "サレド": "THALIDOMIDE",
    "ベルケイド": "BORTEZOMIB",
    "カイプロリス": "CARFILZOMIB",
    "ニンラーロ": "IXAZOMIB",
    "ネクサバール": "SORAFENIB",
    "スーテント": "SUNITINIB",
    "ヴォトリエント": "PAZOPANIB",
    "スチバーガ": "REGORAFENIB",
    "レンビマ": "LENVATINIB",
    "インライタ": "AXITINIB",
    "カボメティクス": "CABOZANTINIB",
    "タキソール": "PACLITAXEL",
    "タキソテール": "DOCETAXEL",
    "ランダ": "CISPLATIN",
    "パラプラチン": "CARBOPLATIN",
    "エルプラット": "OXALIPLATIN",
    "アドリアシン": "DOXORUBICIN",
    "エピルビシン": "EPIRUBICIN",
    "オンコビン": "VINCRISTINE",
    "エトポシド": "ETOPOSIDE",
    "ジェムザール": "GEMCITABINE",
    "ゼローダ": "CAPECITABINE",
    "ティーエスワン": "TEGAFUR",
    "ユーエフティ": "TEGAFUR",
    "カンプト": "IRINOTECAN",
    "トポテシン": "TOPOTECAN",
    "ノルバデックス": "TAMOXIFEN",
    "フェアストン": "TOREMIFENE",
    "アリミデックス": "ANASTROZOLE",
    "フェマーラ": "LETROZOLE",
    "アロマシン": "EXEMESTANE",
    "ゾラデックス": "GOSERELIN",
    "リュープリン": "LEUPRORELIN",
    "カソデックス": "BICALUTAMIDE",
    "イクスタンジ": "ENZALUTAMIDE",
    "ザイティガ": "ABIRATERONE",

    # ボンゾール（ダナゾール）
    "ボンゾール": "DANAZOL",

    # バレオン（ロメリジン）
    "バレオン": "LOMERIZINE",

    # セロシオン（塩酸セビメリン）
    "セロシオン": "CEVIMELINE",

    # ピメノール（プロカテロール系かもしれないが確認必要）
    # メタライトはバリウム製剤

    # テストステロン
    "メチルテストステロン": "METHYLTESTOSTERONE",
}

# 半角カタカナ → 全角カタカナ 変換表
HALFWIDTH_TO_FULLWIDTH = {
    'ｱ': 'ア', 'ｲ': 'イ', 'ｳ': 'ウ', 'ｴ': 'エ', 'ｵ': 'オ',
    'ｶ': 'カ', 'ｷ': 'キ', 'ｸ': 'ク', 'ｹ': 'ケ', 'ｺ': 'コ',
    'ｻ': 'サ', 'ｼ': 'シ', 'ｽ': 'ス', 'ｾ': 'セ', 'ｿ': 'ソ',
    'ﾀ': 'タ', 'ﾁ': 'チ', 'ﾂ': 'ツ', 'ﾃ': 'テ', 'ﾄ': 'ト',
    'ﾅ': 'ナ', 'ﾆ': 'ニ', 'ﾇ': 'ヌ', 'ﾈ': 'ネ', 'ﾉ': 'ノ',
    'ﾊ': 'ハ', 'ﾋ': 'ヒ', 'ﾌ': 'フ', 'ﾍ': 'ヘ', 'ﾎ': 'ホ',
    'ﾏ': 'マ', 'ﾐ': 'ミ', 'ﾑ': 'ム', 'ﾒ': 'メ', 'ﾓ': 'モ',
    'ﾔ': 'ヤ', 'ﾕ': 'ユ', 'ﾖ': 'ヨ',
    'ﾗ': 'ラ', 'ﾘ': 'リ', 'ﾙ': 'ル', 'ﾚ': 'レ', 'ﾛ': 'ロ',
    'ﾜ': 'ワ', 'ｦ': 'ヲ', 'ﾝ': 'ン',
    'ﾞ': '゛', 'ﾟ': '゜',
    'ｧ': 'ァ', 'ｨ': 'ィ', 'ｩ': 'ゥ', 'ｪ': 'ェ', 'ｫ': 'ォ',
    'ｬ': 'ャ', 'ｭ': 'ュ', 'ｮ': 'ョ', 'ｯ': 'ッ', 'ｰ': 'ー',
}

# 濁音・半濁音の組み合わせ
DAKUTEN_MAP = {
    ('カ', '゛'): 'ガ', ('キ', '゛'): 'ギ', ('ク', '゛'): 'グ', ('ケ', '゛'): 'ゲ', ('コ', '゛'): 'ゴ',
    ('サ', '゛'): 'ザ', ('シ', '゛'): 'ジ', ('ス', '゛'): 'ズ', ('セ', '゛'): 'ゼ', ('ソ', '゛'): 'ゾ',
    ('タ', '゛'): 'ダ', ('チ', '゛'): 'ヂ', ('ツ', '゛'): 'ヅ', ('テ', '゛'): 'デ', ('ト', '゛'): 'ド',
    ('ハ', '゛'): 'バ', ('ヒ', '゛'): 'ビ', ('フ', '゛'): 'ブ', ('ヘ', '゛'): 'ベ', ('ホ', '゛'): 'ボ',
    ('ハ', '゜'): 'パ', ('ヒ', '゜'): 'ピ', ('フ', '゜'): 'プ', ('ヘ', '゜'): 'ペ', ('ホ', '゜'): 'ポ',
    ('ウ', '゛'): 'ヴ',
}


def halfwidth_to_fullwidth_katakana(text: str) -> str:
    """半角カタカナを全角カタカナに変換

    Args:
        text: 半角カタカナを含む文字列

    Returns:
        全角カタカナに変換された文字列
    """
    if not text:
        return ""

    # まず単純な文字変換
    result = []
    for char in text:
        result.append(HALFWIDTH_TO_FULLWIDTH.get(char, char))

    # 濁点・半濁点の結合
    final = []
    i = 0
    while i < len(result):
        char = result[i]
        if i + 1 < len(result):
            next_char = result[i + 1]
            combined = DAKUTEN_MAP.get((char, next_char))
            if combined:
                final.append(combined)
                i += 2
                continue
        final.append(char)
        i += 1

    return ''.join(final)


def translate_japanese_to_english(name: str) -> str:
    """日本語薬物名を英語に変換

    Args:
        name: 日本語薬物名（カタカナ、半角または全角）

    Returns:
        英語薬物名、見つからない場合は元の名前
    """
    if not name:
        return ""

    # 1. 半角カタカナを全角に変換
    name = halfwidth_to_fullwidth_katakana(name)

    # 2. 全角数字・記号を除去して基本名を抽出
    base_name = re.sub(r'[０-９0-9]+', '', name)
    # 剤形・単位を除去（錠、カプセル、mg、ΜＧ、顆粒、散、注、液、etc.）
    base_name = re.sub(r'[錠カプセル顆粒散注液軟膏クリームゲル点眼シロップドライ].*$', '', base_name)
    base_name = re.sub(r'[％%ｇgＧmgＭＧμgΜＧmlＭＬ].*$', '', base_name, flags=re.IGNORECASE)
    base_name = base_name.strip()

    # 3. 辞書で検索
    if base_name in JAPANESE_DRUG_DICT:
        return JAPANESE_DRUG_DICT[base_name]

    # 4. 部分一致を試行（より長いキーを優先）
    for jp_name in sorted(JAPANESE_DRUG_DICT.keys(), key=len, reverse=True):
        if jp_name in base_name or jp_name in name:
            return JAPANESE_DRUG_DICT[jp_name]

    return name.upper()


def normalize_ingredient(name: str) -> str:
    """標準化單一成分名稱

    處理邏輯：
    1. 移除括號內的同義詞（EQ TO ...）
    2. 移除其他括號內容（如 VIT B2）
    3. 統一大小寫
    4. 移除多餘空白

    Args:
        name: 原始成分名稱

    Returns:
        標準化後的名稱
    """
    if not name:
        return ""

    # 統一全形括號為半形
    name = name.replace("（", "(").replace("）", ")")

    # 移除括號內容（包含 EQ TO 的同義詞、VIT 等）
    # 但保留括號前的主名稱
    name = re.sub(r"\s*\([^)]*\)", "", name)

    # 移除鹽類後綴的多餘資訊（保留鹽類如 HCL, SODIUM 等）
    name = name.strip()

    # 統一大寫
    name = name.upper()

    # 移除多餘空白
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def extract_ingredients(ingredient_str: str) -> List[str]:
    """從主成分略述欄位提取所有成分

    FDA 資料中多成分以 ; 或 ;; 分隔

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        標準化後的成分列表
    """
    if not ingredient_str:
        return []

    # 統一分隔符號
    # 有些用 ;; 有些用 ;
    ingredient_str = ingredient_str.replace(";;", ";").replace("；", ";")

    # 分割
    parts = ingredient_str.split(";")

    # 標準化每個成分
    ingredients = []
    for part in parts:
        normalized = normalize_ingredient(part)
        if normalized and normalized not in ingredients:
            ingredients.append(normalized)

    return ingredients


def extract_primary_ingredient(ingredient_str: str) -> str:
    """提取主要成分（第一個成分）

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        主要成分名稱（標準化後）
    """
    ingredients = extract_ingredients(ingredient_str)
    return ingredients[0] if ingredients else ""


def get_all_synonyms(ingredient_str: str) -> List[Tuple[str, List[str]]]:
    """提取成分及其所有同義詞

    從括號中的 EQ TO 提取同義詞，並嘗試日語→英語翻譯

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        [(主名稱, [同義詞列表]), ...]
    """
    if not ingredient_str:
        return []

    # 統一分隔符號
    ingredient_str = ingredient_str.replace(";;", ";").replace("；", ";")
    parts = ingredient_str.split(";")

    results = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 統一括號
        part = part.replace("（", "(").replace("）", ")")

        # 提取主名稱（括號前的部分）
        main_match = re.match(r"^([^(]+)", part)
        if not main_match:
            continue

        main_name = main_match.group(1).strip()
        main_name_upper = main_name.upper()
        main_name_upper = re.sub(r"\s+", " ", main_name_upper)

        # 提取所有 EQ TO 同義詞
        synonyms = []
        eq_matches = re.findall(r"EQ TO\s+([^)]+)", part, re.IGNORECASE)
        for match in eq_matches:
            syn = match.strip().upper()
            syn = re.sub(r"\s+", " ", syn)
            # 清理可能的尾部括號內容
            syn = re.sub(r"\s*\(.*$", "", syn)
            if syn and syn != main_name_upper:
                synonyms.append(syn)

        # 嘗試日語→英語翻譯（如果主名稱包含日語字符）
        # 包含: 平假名 (\u3040-\u309F), 全角片假名 (\u30A0-\u30FF),
        #       半角片假名 (\uFF65-\uFF9F), 漢字 (\u4E00-\u9FFF)
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\uFF65-\uFF9F\u4E00-\u9FFF]', main_name):
            english_name = translate_japanese_to_english(main_name)
            if english_name != main_name.upper() and english_name not in synonyms:
                synonyms.insert(0, english_name)  # 英語名優先

        results.append((main_name_upper, synonyms))

    return results
