Qt응용프로그람작성

인민대학습당

주체111(2022)년

차 례

# 머 리 말

경애하는 김정은동지께서는 다음과 같이 말씀하시였다.

《과학과 기술의 시대인 오늘에는 과학기술이 모든 부문의 발전을 좌우하며 추동합니다.》(《주체의 사회주의강국건설을 위하여》 제1권 317~318페지)

경애하는 총비서동지께서는 력사적인 당중앙위원회 제8기 제4차전원회의에서 우리 식 사회주의건설을 승리의 다음단계에로 강력히 인도하는 향도적투쟁방침을 명확히 밝혀주시였다.

5개년계획수행의 확고한 담보를 구축하고 국가발전과 인민생활에서 뚜렷한 개변을 이룩하여야 할 무겁고도 방대한 투쟁과업이 나서고있는 지금 하루를 백날, 천날로 주름잡게 하는 원동력이며 비약과 전진의 힘있는 무기인 과학기술이 기관차적역할을 원만히 수행해나가야 한다.

첨단과학기술의 시대, 지식경제시대의 요구에 맞게 인민경제의 현대화, 정보화를 적극 실현하자면 누구나 다 자기 전공분야에서 리용할수 있는 프로그람들을 적극 개발하고 활용해나갈것을 요구하고있다.

특히 다중가동환경에서 리용할수 있는 Qt를 비롯한 각종 프로그람개발언어들에 대한 폭넓고 깊은 지식을 소유하는것이 매우 중요하다.

Qt에서는 도형처리사용자대면부를 풍부하게 작성할수 있으며 여러 프로그람개발언어들과의 련동을 원만히 보장할수 있다.

이 책에서는 일반적인 C/C++프로그람개발언어를 배운 사용자들이 임의의 조작체계에서 실행되는 Qt응용프로그람을 자체로 작성하도록 하는데 목적을 두고 Qt응용프로그람의 구조와 개발환경, 응용실례들에 대하여 서술하였다.

우리는 프로그람개발언어에 대한 더 많은 활용지식을 습득함으로써 우리 식의 프로그람을 개발할데 대한 위대한 장군님의 교시를 철저히 구현하며 정보산업분야의 유능한 프로그람개발전문가들로 준비해나가야 한다.

# 제1장. Qt응용프로그람의 창문현시

## 제1절. Qt응용프로그람의 구조와 개발환경

### 1. Qt응용프로그람의 구조

Qt는 프로그람작성자들이 다중가동환경에서 C++언어로 GUI응용프로그람을 작성할수 있도록 지원해주는 서고이다. Qt는 객체지향성이 강하며 확장하기 쉬운 수많은 응용프로그람형태의 부분품(component)들을 가지고있는것으로 하여 프로그람을 쉽게 작성할수 있도록 지원해준다.

#### 1) Qt응용프로그람구축

모든 C/C++프로그람과 마찬가지로 Qt서고를 리용한 C++프로그람도 main()함수로부터 시작한다. main()함수안에서는 Qt응용프로그람실체를 만들고 사용자대면부인 창문을 표시하는 처리가 서술된다.

GUI응용프로그람의 기본구조는 다음과 같다.

① 우선 하나의 QApplication객체를 창조하여야 한다.

그것은 이 객체가 GUI응용프로그람에서 사건처리를 위한 사건순환고리를 제공하기때문이다. 이 응용프로그람객체는 하나의 응용프로그람에서 꼭 하나만 창조되여야 한다.

QApplication a(argc, argv);

여기서 argc와 argv는 main()함수에서 넘어온 파라메터들이다.

② 다음은 적어도 하나의 창문을 창조하여야 한다.

창문은 QWidget 또는 그것의 파생클라스의 객체로서 창조한다. QWidget은 모든 사용자대면부요소들의 기초클라스이다.

창문부분품이란 틀창문, 대화창과 같은 창문들과 단추, 표식자와 같은 조종체들을 통털어 이르는 말로서 모든 사용자대면부요소들을 일반적으로 가리키는 개념이다.

QWidget객체는 그 자체만으로도 하나의 창문으로 될수 있다. 그러나 QWidget클라스로부터 틀창문을 관리하는 QMainWindow클라스, 대화창문을 관리하는 QDialog클라스, 조종체들을 관리하는 QLabel, QPushButton과 같은 클라스들이 파생된다.

그러므로 응용프로그람창문은 QWidget으로부터 파생된 임의의 클라스의 객체로 창조할수 있다.

③ 창문을 창조한 다음에는 그것의 크기나 위치 등을 설정하고 현시하여야 한다.

여기에서는 창문부분품을 닫을 때 응용프로그람을 자동적으로 끝내도록 하는 응용프로그람의 기본창문을 설정할수도 있다.

④ 다음 기본사건순환고리에 들어가 사건을 처리하도록 하여야 한다.

기본사건순환고리는 창문체계로부터 사건을 받아 응용프로그람의 창문부분품들에 발송한다.

이것은 QApplication의 exec()함수에 의하여 수행된다.

exec()함수는 exit()를 호출하거나 기본창문부분품을 닫으면 기본사건순환고리에서 탈퇴하게 된다. exec()함수는 탈퇴할 때 exit()함수의 파라메터로 넘겨준 값을 돌려주거나 기본창문부분품을 닫아 기본사건순환고리에서 탈퇴하였다면 0을 돌려준다.

⑤ 응용프로그람을 끝낸다.

exec()함수가 되돌리는 값을 main()함수의 돌림값으로 설정하여 응용프로그람을 끝낸다.

Qt응용프로그람구축도구는 응용프로그람을 구축하기 위해 프로젝트화일(.pro)을 만들고 그로부터 Makefile을 만들어내는 기능을 가진 qmake지령이다.

프로젝트화일의 생성은 qmake지령으로 실현할수 있다.

qmake‐project

우와 같은 지령이 실행되면 현재 등록부의 이름이 hello인 경우 hello.pro라는 프로젝트화일이 만들어진다.

Qt프로젝트화일은 qmake체계에서 인식할수 있는 변수값들로 구성된 본문화일이다. 프로젝트화일에 기초하여 조작탁우에서 지령을 qmake hello.pro라고 주면 Makefile이 만들어진다.

#### 2) 신호와 처리부

일반적으로 창문프로그람을 작성할 때 조작체계와의 쌍방향대화(Interaction)방식을 알고 그에 적합한 형식의 처리를 구성하여야 한다.

QApplication객체에 조종이 넘겨지면 그 시각부터 응용프로그람은 대기방식으로 들어가 사용자의 마우스누르기나 건누르기와 같은 사건들을 기다린다. 사용자가 응용프로그람의 사용자대면부(즉 창문부분품들)에 작용을 가하였을 때 조작체계가 프로그람에 알려주는 사건을 신호(signal)라고 부르며 그에 대한 프로그람의 응답처리를 처리부(slot)라고 부른다.

그러므로 프로그람은 조작체계로부터 받을수 있는 신호와 처리부들 그리고 신호와 그에 응답할수 있는 처리부사이의 련결관계들로 구성된다고 볼수 있으며 프로그람을 작성하는 전과정은 신호들을 확정하고 그에 응답하는 처리부를 만들어나가는것이라고 볼수 있다.

SIGNAL()과 SLOT()마크로들은 Qt문법의 한 부분이다.

― signal과 slot에 의한 개체들사이 통신의 실현과 조종

Qt응용프로그람은 QApplication객체와 GUI를 나타내는 여러 창문부분품들로 구성되며 그들사이의 통신을 실현하는데 signal과 slot가 리용된다.

Qt응용프로그람에서 신호와 신호처리부를 련결시키기 위하여 리용되는 connect()함수호출은 다음과 같다.

connect(sender, SIGNAL(signal), receiver, SLOT(slot));

여기서 sender와 receiver는 QObject에 대한 지적자들이며 signal과 slot는 파라메터이름이 없는 함수선언부들이다. 또한 SIGNAL()과 SLOT()마크로들은 자기들의 파라메터들을 문자렬로 변환한다. 객체들사이의 통신을 실현하자면 객체를 나타내는 클라스를 QObject클라스로부터 파생시켜야 하며 클라스선언부에는 반드시 Q_OBJECT마크로를 놓아야 한다.

GUI응용프로그람작성에서는 한 창문부분품의 변경을 다른 창문부분품들에 통지해야 할 경우가 많이 제기된다.

― 신호와 신호처리부의 련결은 여러가지 형식으로 실현할수 있다.

·한개 신호는 많은 신호처리부에 련결될수 있다.

신호가 발생하면 신호처리부들은 임의의 순서로 한번씩 호출된다.

·많은 신호들은 하나의 동일한 신호처리부에 련결될수 있다.

이렇게 되면 여러개의 신호들가운데서 어느 한 신호가 발생해도 신호처리부는 호출된다.

·한 신호는 다른 신호에 련결될수 있다.

첫번째 신호가 발생하면 두번째 신호도 발생한다.

·련결을 제거할수 있다.

리용중에 있던 객체가 기억기에서 제거될 때 Qt는 그 객체가 포함되여있는 모든 신호-신호처리부련결들을 자동적으로 제거하기때문에 disconnect()함수호출은 거의나 필요로 하지 않는다.

신호와 신호처리부가 호상 련결될 때 그것들은 동일한 파라메터를 가져야 한다.

그러나 례외적으로 신호가 신호처리부보다 더 많은 파라메터를 가진다면 뒤부분의 파라메터들은 무시된다.

대응하는 파라메터들의 자료형이 맞지 않거나 신호처리부의 파라메터개수가 신호의 파라메터개수보다 더 많으면 Qt는 실행시에 그에 대한 경고를 내보낸다. 또한 신호와 신호처리부의 파라메터서술에 파라메터이름이 포함되면 번역시에 경고를 내보낸다.

－ 프로그람을 작성할 때에는 자체로 신호를 정의하고 프로그람내부에서 강제로 발생시켜야 할 경우가 많이 제기된다.

그것은 Qt의 고유한 실마리어 emit를 리용하여 다음과 같은 단계들을 거쳐 실현할수 있다.

① 창문부분품클라스에 자체로 정의한 신호를 선언한다.

여기서 중요한것은 클라스의 내부에 반드시 “signals”라는 실마리어를 배치하고 그아래에 신호를 나타내는 함수를 선언하는것이다.

② 창문부분품클라스에 신호에 응답할수 있는 신호처리부를 선언한다.

여기서 중요한것은 클라스의 내부에 반드시 “slots”라는 실마리어를 배치하고 그아래에 신호처리부를 나타내는 함수를 선언하는것이다.

③ 창문부분품클라스의 구축자에서 신호와 신호처리부를 련결한다.

④ 창문부분품클라스의 성원함수를 실현하는 처리에서 신호를 발생시킨다.

이와 같이 Qt응용프로그람작성에서 신호와 처리부의 련결은 효과적인 GUI를 구성하기 위한 방법론을 확립하는데서 중요한 자리를 차지한다.

#### 3) 사건처리부

신호와 신호처리부와 마찬가지로 사건들은 Qt응용프로그람작성의 기초적인 부분이다. Qt의 핵심부는 사용자의 마우스누르기와 건누르기, 창문크기조절 등을 응용프로그람에 알리기 위하여 사건을 발생하며 프로그람에서는 Qt창문부분품들에 정의된 가상함수들을 재정의하여 사건에 대한 응답을 처리할수 있다. Qt응용프로그람에서 사건응답을 위해 작성된 처리함수들을 사건처리부(event handler)라고 부른다. 례를 들면 QWidget에서 발생되는 paint사건에 응답하는 성원함수는 paintEvent()이다. 프로그람의 창문이 처음 표시될 때 Qt핵심부는 자동적으로 paint사건을 발생시켜 도형들을 그리기한다. 그리고 창문부분품의 크기가 변경되거나 다른 창문에 가리워졌다가 다시 나타날 때에도 자동적으로 paint사건이 발생된다. Qt응용프로그람에서는 자료처리를 진행하고 필요한 경우 QWidget:: repaint()나 QWidget::update()를 호출하여 paint사건을 Qt핵심부에 요청하여 발생시킬수 있다. 이 두 함수의 차이점은 repaint()성원함수는 즉시적인 재그리기를 진행한다면 update()는 Qt의 다음번 처리사건을 리용하여 재그리기사건을 설정한다는것이다. Qt사건모형의 강력한 특징의 한가지는 다른 개체가 사건을 전달받기 전에 임의의 한 QObject가 사건을 감시할수 있다는것이다. 그것은 창문부분품객체에서 자기의 자식창문부분품들에서 발생하는 사건을 감시하는 사건려과기에 의하여 구현될수 있다.

즉 installEventFilter()성원함수를 호출하여 감시하려는 객체와 감시조종객체를 등록하면 감시조종객체의 eventFilter()성원함수에서 감시하려는 객체의 사건을 조종한다.

eventFilter()함수의 첫번째 파라메터는 목적지인 자식객체를 나타내며 두번째 파라메터는 전송되는 사건을 나타내므로 함수본체는 객체의 사건접수상태를 조종하는 처리를 구현하여야 한다.

### 2. QT응용프로그람개발환경

#### 1) 대면부설계도구

대부분의 GUI방식의 응용프로그람들은 기본창문과 여러가지 대화창들로 구성된다. 그러므로 프로그람작성자들은 설계단계에서 확정된 대면부의 구조와 조작방법을 구현하여 사용자의 작용에 응답하는 처리프로그람들을 만들어나간다.

대화창프로그람은 순수 코드작성에 의해 만들어질수 있으며 또는 설계도구를 리용하여 만들어질수 있다.

Qt대면부설계도구를 리용하면 대화창설계과정에서 대화창에 대한 검사와 함께 변경이 쉬워지며 프로그람작성속도도 빠르게 할수 있다.

대화창프로그람을 작성하는것은 다음과 같은 기본단계들을 거친다.

·대면형식령역안에 창문부분품들을 배치한다.

·창문부분품들을 배치관리자에 소속시켜 창문부분품들의 위치 및 크기를 자동적으로 조절할수 있게 한다.

·태브순서를 설정한다.

·신호-신호처리부련결을 설정한다.

·대화창의 전용신호처리부들을 대화창클라스의 성원함수로 구현한다.

Qt Designer는 .ui화일형식으로 화일들을 편집하기 위한 시각적인 대면부설계프로그람이다. Qt Designer의 본래 목적은 지루한 GUI응용프로그람작성부분(대화창설계)을 재미있는 기능으로 전환하는것이다. 각 .ui화일에는 단일한 대화창의 XML서술이 들어있다. 사용자대면부번역프로그람 uic는 XML서술로부터 C++코드를 생성하는 응용프로그람의 구축과정에 사용된다.

Qt Designer의 기능은 다음과 같다.

·응용프로그람의 사용자대면부를 위한 프로젝트관리

·처리부의 코드를 직접 작성할수 있도록 Qt Designer가 코드편집기를 제공하는 대면형식창들에서 코드작성

코드는 .ui.h화일들에 보관되고 파생클라스를 작성할 필요가 없어졌다.(필요하다면 작성자가 파생클라스를 만들수 있다.)

·실행시에 .ui화일들을 적재하게 하는 동적대면형식창적재

이것은 기초코드와 분리된 설계전용화의 중요한 기회를 제공한다.

그림 1‐1. Qt Designer의 대면구성

우의 그림에서 보여주는것처럼 Qt Designer는 대면형식창, 창문부분품창, 객체조사창, 속성편집창, 작용/신호-처리부편집창으로 구성되여있다.

Qt Designer는 시각적인 설계도구이지 완전한 통합개발환경이 아니다. 그 목적은 어떤 특별한 도구에 사용자들이 포로되지 않고 될수록 간단하고 강력한 GUI개발을 가능하게 하는것이다. Qt Designer는 GUI설계를 창조하고 수정하기 쉽게 하지만 아직도 필요하다면 일반 본문편집기를 사용하여 같은 결과를 직접 코드로 얻을수 있다.

더 편리하게 하기 위하여 현재 Qt Designer에는 C++편집기를 플라그인(Plug-in)으로서 포함한다. 대면형식창을 생성하거나 편집하려면 Qt Designer를 사용해야 한다. 대면형식창의 코드를 편집하려면 물론 Qt Designer의 C++편집기를 사용할수 있다. 이 기본편집기는 시각적인 대면형식창설계과정과의 엄격한 통합으로부터 분리할수 있게 한다. 그러나 Notepad, Microsoft Visual Studio 등의 편집기를 사용하는것이 좋으면 여전히 그것을 사용할수 있다.

Qt Designer는 .ui화일 실례로 form.ui를 읽고 쓴다. 사용자대면부번역프로그람 uic는 머리부화일 실례로 form.h와 실현화일 실례로 form.cpp를 .ui화일로부터 둘다 창조한다.

main.cpp의 응용프로그람코드는 form.h를 포함한다. 일반적으로 main.cpp는 QApplication객체의 실례를 만들고 사건순환고리를 시작하는데 사용된다.

이 수법은 간단하지만 더 복잡한 대화창에는 충분하지 않다. 복잡한 대화창은 대면형식창의 창문부분품들에 련결된 아주 많은 론리를 가지며 보통 미리 정의된 신호와 처리부들로 보여주는것보다 더 많은 론리를 가지고있다. 이 여유론리를 조종하는 하나의 방법은 대면형식창(form)에 기능을 추가하는 조종자클라스를 응용프로그람코드에 쓰는것이다. 이것은 uic가 생성한 클라스들이 공개부분에 대면형식창의 조종과 그 신호를 내주기때문에 가능하다. 이 수법의 큰 결함은 그것이 정확한 Qt형식이 아닌것이다. Qt Designer를 사용하지 않는다면 대체로 대면형식창자체에 론리를 추가하군 한다. 이것은 대면형식창에 전용처리부들과 성원변수들을 추가하는 능력이 초기에 Qt Designer에 추가되였기때문이다. 이 수법의 중요한 우점은 미리 정의된 처리부에 신호를 련결하는데 사용하던 도형방식으로 Qt Designer를 사용하여 신호를 전용처리부에 련결할수 있는것이다. 그다음 uic는 매개 전용처리부에 대하여 빈 그루터기(stub)를 생성된 form.cpp실현화일에 추가한다. 여기서 큰 문제는 그 전용처리부들에 전용실현코드를 어떻게 추가하는가 하는것이다. 생성된 form.cpp에 코드의 추가는 선택적인것이 아니며 이 화일은 대면형식창이 변경될 때마다 uic에 의하여 다시 생성되며 작성자들은 생성된 코드와 손으로 쓴 코드의 결합을 바라지 않는다.

― ui.h확장수법

유연성과 완전성에도 불구하고 파생클라스작성수법은 일부 결함을 가진다.

·파생클라스작성은 모두에게 자연스럽지 않고 쉽지 않다. 객체지향수법을 새로 배우는 사람들은 파생클라스로 작성하는것을 전용처리부의 실현보다 어려운 일로 생각한다.

·생성된 클라스들을 계승하는것은 프로그람작성오유의 추가적인 원천이다. 특히 재실현함수의 수가 많고 설계과정에 기호가 자주 변경된다면 이것은 더하다. 개발과정을 더 원만하게 하기 위하여 uic는 순수가상함수보다도 전용처리부용 빈 그루터기를 생성한다. 이 수법은 코드의 콤파일(compile) 및 실행을 유지하는 한편 프로그람작성자들은 실행시 경고오유통보문을 놓치는 경우에 부닥치게 되고 파생클라스에서 자그마한 철자오유를 발견하는데 시간을 소비한다.

·수백개의 대면형식창을 가지는 큰 프로젝트들에서 보충적인 파생클라스들은 콤파일속도와 코드크기에서 현저한 차이를 가진다.

.ui화일, form.ui와 함께 Qt Designer는 다른 련관된 화일 form.ui.h을 읽고 쓴다. 이 .ui.h화일은 보통의 C++원천화일로서 전용처리부의 실현을 포함하고 생성된 대현형식창실현화일 form.cpp로부터 포함되므로 다른 사용자코드에서 완전히 무시될수 있다. C++코드를 포함하는 .h확장을 .ui.h화일에 사용하는 리유는 그것이 항상 포함되며 .h확장으로 구축과정에 통합하기 더 쉽기때문이다.

form.ui.h화일은 다른 모든 화일들중에서 특별한 위치를 차지한다. 이것은 사용자와 Qt Designer에 의하여 읽고 씌워지는 공유원천화일로서 일반적으로 수정조종되는 원천화일이며 uic에 의하여 생성되지 않는다. Qt Designer가 할 일은 련관된 대면형식창의 전용처리부정의와 동기하여 화일들을 유지하는것이다.

① 사용자가 대면형식창에 새 처리부를 추가할 때마다 Qt Designer는 .ui.h화일에 그루터기를 추가한다.

② 사용자가 전용처리부의 기호를 변경할 때마다 Qt Designer는 대응하는 실현을 갱신한다.

③ 사용자가 전용처리부를 삭제할 때마다 Qt Designer는 그것을 .ui.h화일에서 삭제한다.

이리하여 완전성이 담보되고 파생클라스를 만들 필요가 없어지고 파생클라스안의 처리부들을 잊어버리거나 철자가 틀릴 위험이 더는 없어진다.

.ui.h화일들은 내부 C++편집기플라그인을 가지고있는 Qt Designer에서 직접 편집하거나 사용자에게 편리한 편집기에서 편집할수 있다. 오직 .ui.h화일에 처리부실현을 삽입하고 Qt Designer안에서 항상 처리부를 추가, 삭제하거나 이름변경하여야 한다.

Qt Designer에서 혹은 자기의 편집기를 사용하여 처리부의 실현을 편집할수 있다.

자체의 편집기를 사용한다면 Qt Designer는 변경을 보관한다.

ui.h확장수법은 파생클라스작성수법에 비하여 한가지 결함을 가지고있다. ui.h화일은 오직 전용처리부실현만 포함하지만 객체는 여전히 생성된 form.cpp코드안에서 구성되고 해체된다. 이것은 보통 C++클라스의 구성자와 해체자에서 수행하는 대면형식창의 초기화나 삭제를 사용자가 할수 없게 한다. 이러한 제한하에서 작업하기 위하여 init/destroy관례를 만들었다. 대면형식창에 처리부 Form::init()를 추가하자면 이 처리부는 생성된 대면형식창구성자의 끝에서 자동적으로 호출된다.

마찬가지로 대면형식창에 처리부 Form::destroy()를 추가하면 처리부는 임의의 대면형식창조종이 삭제되기 전에 자동적으로 호출된다.(이 처리부들은 void를 돌려주어야 한다.) 자체의 편집기를 사용하기 좋아한다면 여전히 Qt Designer에서 이 함수들을 창조한다. Qt Designer의 C++편집기플라그인이나 자체의 편집기를 사용하여 실현코드를 쓸수 있다.

#### 2) 콤파일러(Compiler)도구

－ qmake

수동적인 Makefile작성은 복잡하여 오유를 범하기 쉬우며 특히 각이한 콤파일러들과 가동환경을 결합하여 여러개의 Makefile들을 만들 때는 특히 더 복잡하다. 개발자들은 qmake를 리용하여 간단한 하나의 프로젝트화일을 만들고 qmake를 실행하여 적당한 Makefile들을 생성한다. qmake는 콤파일러와 가동환경의 의존관계들을 모두 고려하여 개발자들이 마음놓고 자기 코드작성에만 집중할수 있게 한다.

qmake는 또한 moc와 uic의 구축규칙들을 자동적으로 포함하여 Qt의 특수한 요구를 만족시킨다.

응용프로그람의 출하판은 오유수정기호나 다른 오유수정정보를 포함하지 않는다.

개발시에 관련정보를 가지는 응용프로그람의 오유수정판을 생성하는것이 좋다. 이것은 프로젝트화일안의 CONFIG변수에 'debug'를 추가하여 간단히 달성된다.

Makefile을 생성하기 전에 qmake를 사용하여 자기 응용프로그람을 오유수정가능하게 할수 있다.

자기 응용프로그람의 가동환경에 고유한 코드부분을 만들어 가동환경에 의존하는 코드를 분리하여 만들려고 결심할수 있다. 그러면 자기의 프로젝트화일에 포함해야 할 화일이 두개로 된다. 즉 hellowin.cpp와 hellounix.cpp를 들수 있다. SOURCES변수에 이것들을 추가하면 Makefile에 두 화일이 모두 넣어지므로 그렇게 할수 없다. 그러므로 여기서 할 일은 qmake를 실행하는 가동환경에 따라서 처리되는 유효범위를 리용하는것이다.

Makefile을 생성하기 전에 qmake를 사용하여야 한다.

어떤 화일이 존재하지 않으면 Makefile을 창조하지 않으려고 할수 있다. exists()함수에 의하여 화일이 있는가 검사할수 있다. error()함수를 사용함으로써 qmake의 처리를 중지시킬수 있다. 이것은 유효범위와 같은 수법으로 작업한다. 단순히 유효범위조건을 함수로 바꾸면 된다. main.cpp화일의 검사는 다음과 같다.

!exists(main.cpp) {

error( "No main.cpp file found" )

}

!는 본문을 부정하는데 쓰인다. 즉 exists(main.cpp)는 화일이 존재하면 참이 고 !exists(main.cpp)은 화일이 존재하지 않으면 참이다.

－ 메타객체콤파일러 moc

메타객체콤파일러(Meta Object Compiler) moc는 Qt의 C++확장을 조종하는 프로그람이다.

moc는 C++원천화일을 읽어들인다. 그것이 Q_OBJECT마크로를 포함하는 하나이상의 클라스선언을 발견하면 Q_OBJECT마크로를 사용하는 클라스들에 대한 메타객체코드를 포함하는 다른 C++원천화일을 생성한다. 다른것들중에서 메타객체코드는 신호-처리부기구, 실행시 형정보 및 동적속성체계에 요구된다.

moc가 생성한 C++원천화일은 클라스의 실현과 함께 콤파일되고 련결되여야 한다. 혹은 클라스의 원천화일에 포함(include)될수 있다.

qmake를 사용하여 자기의 Makefile들을 창조한다면 필요할 때 moc를 호출하는 구축규칙들이 포함되므로 moc를 직접 사용할 필요가 없다.

자기 프로그람의 Makefile에 규칙들을 추가함으로써 make는 필요할 때 moc의 실행과 moc출력의 조종을 고려할수 있다.

Makefile들을 자체로 창조하려고 한다면 여기에 moc조종을 포함하는 방법에 대한 암시가 있다.

머리부화일안의 Q_OBJECT클라스선언에 대하여서는 아래에 GNU make를 사용하는 경우에만 쓸모있는 Makefile이 있다.

moc_%.cpp: %.h

moc $< -o $@

이식할수 있게 하려면 다음의 형식으로 독특한 규칙들을 사용할수 있다.

moc_NAME.cpp: NAME.h

moc $< -o $@

또한 자기의 SOURCES(자기가 애호하는 이름을 대리)변수에 moc_NAME.cpp를, OBJECTS변수에 moc_NAME.o 혹은 moc_NAME.obj를 추가하는것을 기억하여야 한다.(C++원천화일들을 .cpp라고 이름짓기를 좋아하여도 moc가 그것을 고려하지 않으므로 .C, .cc, .CC, .cxx 혹은 .c++를 사용할수도 있다.)

실현화일(.cpp)의 Q_OBJECT클라스선언에서는 다음과 같은 Makefile규칙을 제안한다.

NAME.o: NAME.moc

NAME.moc: NAME.cpp

moc -i $< -o $@

이것은 NAME.cpp을 콤파일하기 전에 make가 moc를 실행한다는것을 담보한다.

그다음 NAME.cpp의 끝에 다음 행을 넣을수 있다.

#include "NAME.moc"

그 화일에서 선언한 모든 클라스들은 충분히 알려져있다.

― 사용자대면부콤파일러 uic

uic는 Qt Designer에 의해 생성된 XML로 된 사용자대면부정의화일(.ui)을 읽어들이고 대응하는 C++머리부화일 혹은 원천화일들을 창조한다. 또한 화상화일을 생성하여 C++원천코드에 생화상자료를 매몰한다.

uic [options] <file>

uic [options] -impl <headerfile> <file>

uic [options] -embed <project> <image1> <image2> <image3>

uic [options] -subdecl <classname> <headerfile> <file>

uic [options] -subimpl <classname> <headerfile> <file>

uic는 make에 의해서만 호출된다.

여기에 GNU make만 사용한다면 Makefile을 사용할수 있다.

%.h: %.ui

uic $< -o $@

%.cpp: %.ui

uic -impl $*.h $< -o $@

이식가능하게 쓰려면 다음 형식의 개별적인 규칙들을 사용할수 있다.

NAME.h: NAME.ui

uic $< -o $@

NAME.cpp: NAME.ui

uic -impl $*.h $< -o $@

자기의 SOURCES(자기가 좋아하는 이름을 대리)변수에 NAME.cpp를, 자기의 OBJECTS변수에 NAME.o을 추가하는것을 잊지 말아야 한다.(C++원천화일을 .cpp로 이름짓는것을 좋아해도 uic는 고려하지 않으므로 C, .cc, .CC, .cxx 혹은 자기에게 좋으면 지어는 .c++를 사용할수 있다.)

## 제2절. 대화창

대화창은 사용자에게 자기가 좋아하는 값들을 선택할 기회를 준다. 대부분의 GUI응용프로그람들은 차림표띠와 도구띠를 가지는 하나의 기본창문과 기본창문을 보충하는 한 조의 대화창으로 이루어진다. 또한 적당한 작용들을 수행함으로써 사용자의 선택에 직접 응답하는 대화창프로그람들을 작성할수 있게 한다.

일반적으로 대화창은 정보를 되돌리거나 리용자로부터 입력내용을 얻는 하나의 특수한 창문이다. 대화창에는 일반적으로 단행정보를 현시하는 대화창과 복잡한 조종요소를 포함하는 대형대화창 등 여러가지 형태와 크기를 가진 대화창들이 있다.

비교적 큰 GUI응용프로그람에는 체계선택항목의 설치, 서체의 설치, 형태의 설치와 각종 형식의 안내 등 각이한 대화기능을 제공하는 대화창들이 있다.

### 1. 자체정의한 대화창

QDialog는 모든 Qt대화창의 기초클라스로서 QWidget로부터 계승된다.

QDialog클라스는 대화창을 제공하는 클라스이다.

QDialog클라스의 구성자는 다음과 같다.

QDialog (QWidget *parent=0, const char * name=0, bool modal=FALSE, WFlags f =0)

QDialog클라스의 show()함수는 modal속성에 따라 모달형대화창 또는 비모달형대화창을 현시하고 인차 되돌려진다. exec()함수는 모달형대화창으로 현시하며 사용자가 대화창을 닫기 전에는 되돌려지지 않으며 되돌려질 때에는 대화창에서 변경된 설정들을 접수하는가, 접수하지 않는가를 가리키는 모달대화창의 결과코드(Accepted, Rejected)를 돌려준다. 모달대화창의 결과코드는 result()함수에 의하여 얻을수 있고 setResult()함수에 의하여 설정할수 있다.

가상함수 accept()는 모달대화창을 숨기고 결과코드를 Accepted로 설정하며 가상함수 reject()는 모달대화창을 숨기고 결과코드를 Rejected로 설정한다.

가상함수 done()은 대화창을 닫고 파라메터에 넘어온 값으로 결과코드를 설정하며 대화창이 exec()함수로 현시되였다면 exec()함수를 끝내고 이 결과코드를 돌리도록 한다.

QMessageBox클라스는 정보를 현시하는 다음과 같은 여러가지 방식의 통보창들을 제공한다.

QMessageBox::about는 제목과 간단한 문장이 있는 통보창인데 일반적으로 도움말통보창에 쓰인다.

QMessageBox::information는 제목과 알림문을 현시하는 통보창이다.

QMessageBox::warning는 제목과 정보의 경고통보창이다.

QMessageBox::critical는 제목과 정보의 오유통보창이다.

색대화창 QColorDialog은 리용자가 색을 선택할수 있게 한다.

오유통보창 QErrorMessage는 오유정보를 현시한다.

화일대화창 QFileDialog는 리용자가 한개 또는 여러개의 화일과 목록들을 선택할수 있게 한다.

서체대화창 QFontDialog는 리용자가 서체를 선택하거나 설정할수 있게 한다.

입력대화창 QInputDialog는 리용자가 간단한 입력(실례로 한행의 본문 또는 한개 수자 등)을 진행하게 한다.

페지설정대화창 QPageSetupDialog는 페지와 련결된 인쇄기선택항목을 배치한다.

진행대화창 QProgressDialog는 리용자에게 조작진행과정과 이 조작이 이미 끝났는가를 보여준다. 인쇄기대화창 QPrintDialog는 인쇄기를 배치하며 리용자가 리용가능한 인쇄기를 선택하게 하며 리용자가 문서와 관련한 설정(종이의 크기와 방향 등), 인쇄류형설정(천연색인쇄 또는 흑색인쇄), 페지수범위와 인쇄할 부수 등을 설정하게 한다.

대화창을 클라스로서 실현함으로써 대화창을 자체의 신호와 처리부를 가지는 독립적이고도 필요한 모든것을 다 갖춘 부분품으로 만든다.

검색대화창의 원천코드는 다음과 같다.

#include <qcheckbox.h>

#include <qlabel.h>

#include <qlayout.h>

#include <qlineedit.h>

#include <qpushbutton.h>

#include "finddialog.h"

FindDialog::FindDialog(QWidget *parent, const char *name)

: QDialog(parent, name) {

setCaption(tr("Find"));

label = new QLabel(tr("Find &what:"), this);

lineEdit = new QLineEdit(this);

label→setBuddy(lineEdit);

caseCheckBox = new QCheckBox(tr("Match &case"), this);

backwardCheckBox = new QCheckBox(tr("Search &backward"), this);

findButton = new QPushButton(tr("&Find"), this);

findButton→setDefault(true); findButton→setEnabled(false);

closeButton = new QPushButton(tr("Close"), this);

connect(lineEdit, SIGNAL(textChanged(const QString &)),

this, SLOT(enableFindButton(const QString &)));

connect(findButton, SIGNAL(clicked()), this, SLOT(findClicked()));

connect(closeButton, SIGNAL(clicked()), this, SLOT(close()));

QHBoxLayout *topLeftLayout = new QHBoxLayout;

topLeftLayout→addWidget(label);

topLeftLayout→addWidget(lineEdit);

QVBoxLayout *leftLayout = new QVBoxLayout;

leftLayout→addLayout(topLeftLayout);

leftLayout→addWidget(caseCheckBox);

leftLayout→addWidget(backwardCheckBox);

QVBoxLayout *rightLayout = new QVBoxLayout;

rightLayout→addWidget(findButton); rightLayout→addWidget(closeButton);

rightLayout→addStretch(1);

QHBoxLayout *mainLayout = new QHBoxLayout(this);

mainLayout→setMargin(11);

mainLayout→setSpacing(6);

mainLayout→addLayout(leftLayout); mainLayout→addLayout(rightLayout);

}

문자렬주위의 tr()함수는 문자렬을 여러가지 언어로 번역할수 있게 한다. tr()함수는 Q_OBJECT마크로를 포함하는 QObject와 그 파생클라스에서 선언된다.

다음으로 자식창문부분품들을 만든다. &기호를 사용하여 지름건을 지적한다. 짝패(buddy)는 표식자의 지름건을 누를 때 초점을 받아들이는 창문부분품이다. 그러므로 사용자가 Alt+W(표식자의 지름건)를 누를 때 초점은 행편집기(짝패)로 간다.

setDefault(true)를 호출함으로써 Find단추를 대화창의 기정단추(default button)로 만든다. 기정단추는 사용자가 Enter건을 누를 때 눌리우는 단추이다.

비공개처리부 enableFindButton(const QString &)은 행편집기안의 본문이 달라질 때마다 호출된다. 비공개처리부 findClicked()는 사용자가 Find단추를 찰칵할 때 호출된다. 대화창은 사용자가 Close를 찰칵할 때 닫긴다. close()처리부는 QWidget로부터 파생되고 그 기정동작은 창문부분품을 숨기는것이다.

QObject는 FindDialog의 기초클라스이므로 connect()호출앞에서 QObject::앞붙이를 생략할수 있다.

대화창의 처리부는 다음과 같다.

void FindDialog::findClicked() {

QString text = lineEdit→text();

bool caseSensitive = caseCheckBox→isOn();

if (backwardCheckBox→isOn())

emit findPrev(text, caseSensitive);

else

emit findNext(text, caseSensitive);

}

void FindDialog::enableFindButton(const QString &text) {

findButton→setEnabled(!text.isEmpty());

}

findClicked()처리부는 사용자가 Find단추를 찰칵할 때 호출된다. 이때 Search backward선택에 따라서 findPrev() 혹은 findNext()신호를 발생한다. emit예약어는 Qt에 고유한것으로서 다른 Qt확장기능처럼 C++앞처리기에 의해 표준 C++로 변환된다.

enableFindButton()처리부는 사용자가 행편집기안의 본문을 변경할 때마다 호출된다. 이 처리부는 편집기안에 본문이 있으면 단추를 허용하고 그렇지 않으면 금지한다.

이제는 main.cpp화일을 창조하여 FindDialog창문부분품을 시험해볼수 있다.

#include <qapplication.h>

#include "finddialog.h"

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

FindDialog *dialog = new FindDialog;

app.setMainWidget(dialog);

dialog→show();

return app.exec();

}

### 2. 대화창의 고속설계

Qt Designer를 기동시키고 Dialog형판을 선택하면 Form1창문이 나타난다.

첫 단계에서는 자식창문부분품들을 창조하여 대면형식창우에 배치한다. 본문표식자(text label) 하나, 행편집기(line editor) 하나, (수평)수축자(spacer) 하나 그리고 두개의 누름단추(pushbutton)들을 창조한다.

Qt Designer의 기본창문오른쪽에 있는 속성편집기에 의하여 각 창문부분품의 속성들을 설정한다.

① 본문표식자를 찰칵하고 name속성을 label로, text속성을 "&Cell Location:"로 설정한다.

② 행편집기를 찰칵하고 name속성을 lineEdit로 설정한다.

③ 수축자를 찰칵하고 수축자의 orientation속성이 Horizontal로 설정되였는가를 확인한다.

④ 첫째 단추를 찰칵하고 name속성을 okButton으로, enabled속성을 False로, default속성을 True로, text속성을 OK로 설정한다.

⑤ 둘째 단추를 찰칵하고 name속성을 cancelButton으로, text속성을 Cancel로 설정한다.

⑥ 대면형식창의 배경을 찰칵하여 대면형식창자체를 선택하고 name속성을 GoToCellDialog로, caption속성을 "Go to Cell"로 설정한다.

"&Cell Location"을 표시하는 본문표식자를 제외한 모든 창문부분품들이 잘 보인다. Tools|Set Buddy를 찰칵한다. 표식자를 누른 상태에서 마우스를 행편집기까지 끌고가서 놓는다. 그러면 행편집기는 표식자의 짝패로 된다. 표식자의 buddy속성이 lineEdit로 설정되였는가를 검사하여 이것을 확인할수 있다.

신호–처리부련결들을 설정하고 사용자정의처리부들을 실현하여 대면형식창이 동작하게 하는 부분만이 남는다. Edit|Connections를 찰칵하여 련결편집기를 펼친다.

련결을 창조하려면 New단추를 찰칵하고 내리펼침복합칸들을 리용하여 Sender와 Signal, Receiver, Slot마당들을 설정한다.

OkButton의 clicked()신호를 GoToCellDialog의 accept()처리부에 련결한다.

cancelButton의 clicked()신호를 GoToCellDialog의 reject()처리부에 련결한다. Edit Slots를 찰칵하여 Qt Designer의 처리부편집기를 펼치고 enableOkButton()비공개처리부를 창조한다. 끝으로 lineEdit의 textChanged(const QString &)신호를 GoToCellDialog의 새로운 enableOkButton()처리부에 련결한다.

대화창을 미리 보려면 Preview|Preview Form차림표선택을 찰칵한다. Tab를 반복하여 눌러서 태브순서를 검사한다. Alt+C를 눌러서 초점을 행편집기로 옮긴다. Cancel을 찰칵하여 대화창을 닫는다.

대화창을 gotocell이라는 등록부에 gotocelldialog.ui로서 보관하고 일반본문편집기에 의하여 같은 등록부에 main.cpp화일을 창조한다.

#include <qapplication.h>

#include "gotocelldialog.h"

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

GoToCellDialog *dialog = new GoToCellDialog;

app.setMainWidget(dialog);

dialog→show();

return app.exec();

}

qmake를 실행하여 .pro화일과 Makefile을 창조한다.

Qt Designer리용의 한가지 우점은 원천코드를 혼돈시키지 않고 프로그람작성자들이 대면형식창설계를 수정할 권한을 얻는다는데 있다. C++코드를 쓰는 방법으로 순수 대면형식창을 개발할 때 설계에 대한 변경은 시간을 소비하게 한다. Qt Designer를 리용할 때 uic는 변경된 대면형식창들에 대해서만 원천코드를 재생하므로 시간을 랑비하지 않는다.

이제 프로그람을 실행하면 대화창은 동작하지만 요구대로 정확한 기능을 수행하지 않는다.

·OK단추는 항상 비능동상태로 된다.

·행편집기는 유효세포위치들만 받아들일 대신에 임의의 본문을 다 받아들인다.

그러므로 이 문제를 해결하기 위한 코드를 써야 한다.

대면형식창의 배경을 두번 련속 찰칵하여 Qt Designer의 코드편집기를 펼친다. 편집기창문에서 다음의 코드를 입력한다.

#include <qvalidator.h>

void GoToCellDialog::init() {

QRegExp regExp("[A–Za–z] [1–9] [0–9] {0, 2}");

lineEdit→setValidator(new QRegExpValidator(regExp, this));

}

void GoToCellDialog::enableOkButton() {

OkButton→setEnabled(lineEdit→hasAcceptableInput());

}

init()함수가 대면형식창구성자(uic가 생성)의 끝에서 자동적으로 호출된다. 입력범위를 제한하기 위하여 유효기를 설정한다. Qt는 3개의 기본유효성확인클라스 즉 QIntValidator와 QDoubleValidator, QRegExpValidator를 제공한다. 여기서는 정규식 "[A-Za-z][1-9][0-9]{0,2}"을 가지고 QRegExpValidator를 리용한다. 이것은 하나의 영문자와 그뒤에 1～999까지의 수값으로 이루어진 값만이 유효하다는것을 의미한다.

이것을 QRegExpValidator구성자에 넘김으로써 GoToCellDialog객체의 자식으로 만든다. 그리하여 후에 QRegExpValidator의 부모가 삭제될 때 자동적으로 삭제된다.

enableOkButton()처리부는 행편집기가 유효세포위치를 포함하는가에 따라서 OK단추를 허용 혹은 금지한다. QLineEdit::hasAcceptableInput()는 init()함수에서 설정한 유효기를 사용한다.

코드를 입력한 후에 다시 대화창을 보관한다. 이때 2개 화일 즉 사용자대면부화일 gotocelldialog.ui와 C++원천화일 gotocelldialog.ui.h를 보관한다. 다시 응용프로그람을 구축하고 실행한다. 행편집기에 "A12"라고 입력하면 OK단추가 능동상태로 되는것을 알수 있다. Cancel을 찰칵하여 대화창을 닫는다.

이 실례에서는 Qt Designer에서 대화창을 편집하고 Qt Designer의 코드편집기에 의하여 코드를 추가하였다. 대화창의 사용자대면부는 .ui화일(XML기초화일형식)에 보관되고 코드는 .ui.h화일(C++원천화일)에 보관된다.

.ui.h의 다른 수법은 보통과 같이 Qt Designer로 .ui화일들을 창조하고 uic가 생성한 클라스를 계승하는 파생클라스를 창조하고 거기에 나머지 기능을 추가하는것이다. 례를 들면 Go-to-Cell대화창에서 이것은 GoToCellDialog를 계승하는 GoToCellDialogImpl클라스를 창조하여 필요한 기능을 추가적으로 실현한다는것을 의미한다.

## 제3절. 기본창문

### 1. QMainWindow의 파생클라스만들기

응용프로그람의 기본창문은 QMainWindow의 파생클라스로서 창조한다.

표계산프로그람에서 기본창문의 원천코드는 다음과 같다.

MainWindow클라스를 QMainWindow의 파생클라스로서 정의한다. 이것은 자체의 신호와 처리부를 제공하므로 Q_OBJECT마크로를 포함한다.

closeEvent()함수는 사용자가 창문을 닫을 때 자동적으로 호출되는 QWidget의 가상함수이다. 이것은 MainWindow에서 사용자에게 표준질문 "Do you want to save your changes?"를 표시하고 디스크에 사용자의 선택을 보관하도록 재정의한다.

마찬가지로 contextMenuEvent()함수는 사용자가 창문부분품을 오른쪽단추로 찰칵하거나 가동환경에 고유한 차림표건을 누를 때 호출된다. 이것은 MainWindow에서 차림표를 펼치도록 재정의된다.

File|New와 Help|About와 같은 일부 차림표선택들은 MainWindow에서 비공개처리부들로서 실현된다. 대부분의 처리부들은 돌림값으로서 void를 가지지만 save()와 saveAs()는 bool을 돌려준다. 돌림값은 신호에 응답하여 처리부가 실행될 때 무시되지만 함수로서 처리부를 호출할 때 돌림값은 보통의 C++함수를 호출할 때처럼 사용할수 있다.

기본창문은 사용자대면부를 유지하기 위한 많은 비공개처리부들과 여러개의 비공개함수들을 요구한다. 또한 MainWindow는 비공개처리부, 비공개함수들과 함께 수많은 비공개변수들을 가진다.

#include <qaction.h>

#include <qapplication.h>

#include <qcombobox.h>

#include <qfiledialog.h>

#include <qlabel.h>

#include <qlineedit.h>

#include <qmenubar.h>

#include <qmessagebox.h>

#include <qpopupmenu.h>

#include <qsettings.h>

#include <qstatusbar.h>

#include "cell.h"

#include "finddialog.h"

#include "gotocelldialog.h"

#include "mainwindow.h"

#include "sortdialog.h"

#include "spreadsheet.h"

MainWindow::MainWindow(QWidget *parent, const char *name) :

QMainWindow(parent, name) {

spreadsheet = new Spreadsheet(this);

setCentralWidget(spreadsheet);

createActions(); createMenus();

createToolBars(); createStatusBar();

readSettings(); setCaption(tr("Spreadsheet"));

setIcon(QPixmap::fromMimeSource("icon.png"));

findDialog = 0; fileFilters = tr("Spreadsheet files (*.sp)");

modified = false;

}

구성자에서는 Spreadsheet창문부분품을 창조하여 기본창문의 중심창문부분품으로 설정하는것으로 시작한다. 중심창문부분품은 도구띠들과 상태띠사이의 구역을 차지한다. Spreadsheet클라스는 표계산식들의 유지와 같은 표계산능력을 갖춘 QTable의 파생클라스이다.

그다음 비공개함수들인 createActions(), createMenus(), createToolBars(), createStatusBar()를 호출하여 기본창문의 나머지를 창조한다. 또한 비공개함수readSettings()를 호출하여 기억되여있는 응용프로그람의 환경설정을 읽어들인다.

창문의 그림기호를 PNG화일인 icon.png로 설정한다. Qt는 BMP, GIF, JPEG, MNG, PNG, PNM, XBM 및 XPM을 비롯한 수많은 화상형식을 제공한다. QWidget::setIcon()을 호출하여 창문의 왼쪽웃구석에 그림기호가 표시되게 설정한다. 가동환경에 의존하지 않고 탁상우에 나타나는 응용프로그람그림기호를 설정하는 방법은 없다.

일반적으로 GUI응용프로그람들은 수많은 화상들을 사용하고 일부 화상은 여러개의 다른 경우에 사용된다. Qt는 응용프로그람에 화상을 제공하는 여러가지 방법을 가지고있다.

가장 일반적인 방법은 다음과 같다.

·화일들에 화상을 보관하였다가 실행시에 적재하기

·원천코드에 XPM화일들을 포함하기(이것은 XPM화일들도 유효한 C++화일들이므로 제대로 동작한다.)

·Qt의 《화상집합》기구의 사용

여기서는 실행시에 화일을 적재하는것보다 간단하면서 효과적인 화상집합수법을 리용한다. 이것은 유지되여있는 화일형식으로 작업한다. 화상들은 images라고 부르는 보조등록부안의 원천나무에 보관된다.

응용프로그람의 .pro화일에 다음의 코드

IMAGES = images/icon.png \

images/new.png \

images/open.png \

...

images/find.png \

images/gotocell.png

를 추가함으로써 uic가 지정된 화상모두에 대한 자료를 포함하는 C++원천코드화일을 생성하게 한다.

그다음 자료는 응용프로그람의 실행화일로 콤파일되고 QPixmap:: fromMimeSource()에 의하여 얻을수 있다. 이것은 그림기호와 기타 화상들이 적재되여 항상 실행가능상태에 있다는 우점이 있다.

Qt Designer에 의하여 대화창은 물론 기본창문을 창조한다면 그것을 리용하여 .pro화일을 조종할수 있고 화상들을 화상집합에 시각적으로 추가할수 있다.

### 2. 차림표와 도구띠의 만들기

대부분의 GUI응용프로그람들은 차림표와 도구띠를 모두 제공하며 일반적으로 차림표와 도구띠는 같은 지령들을 포함한다. 차림표는 사용자들이 응용프로그람을 조사하고 새로운 기능을 호출할수 있게 하고 도구띠는 흔히 사용하는 기능에 대한 고속호출을 제공한다.

Qt는 《작용》개념을 통하여 차림표와 도구띠의 프로그람작성을 단순화한다. 작용(action)은 하나의 차림표, 하나의 도구띠 혹은 차림표와 도구띠에 모두 추가할수 있는 항목이다. Qt에서 차림표와 도구띠는 다음과 같은 단계를 통하여 창조된다.

·작용들을 창조한다.

·작용들을 차림표에 추가한다.

·작용들을 도구띠에 추가한다.

표계산프로그람에서 작용들은 createActions()에서 창조된다.

void MainWindow::createActions(){

newAct = new QAction(tr("&New"), tr("Ctrl+N"), this);

newAct→setIconSet(QPixmap::fromMimeSource("new.png"));

newAct→setStatusTip(tr("Create a new spreadsheet file"));

connect(newAct, SIGNAL(activated()), this, SLOT(newFile()));

showGridAct = new QAction(tr("&Show Grid"), 0, this);

showGridAct→setToggleAction(true);

showGridAct→setOn(spreadsheet→showGrid());

showGridAct→setStatusTip(tr("Show or hide the spreadsheet's grid"));

connect(showGridAct, SIGNAL(toggled(bool)), spreadsheet, SLOT(setShowGrid)));

aboutQtAct = new QAction(tr("About &Qt"), 0, this);

aboutQtAct→setStatusTip(tr("Show the Qt library의 About box"));

connect(aboutQtAct, SIGNAL(activated()), qApp, SLOT(aboutQt()));

}

New작용은 작용이름(New), 지름건(Ctrl+N), 부모(기본창문), 그림기호(new.png), 그리고 상태암시를 가진다. 작용의 activated()신호를 기본창문의 비공개성원 newFile()처리부에 련결한다.

련결이 없으면 사용자가 File|New차림표항목을 선택하거나 New도구띠단추를 찰칵할 때 아무런 반응도 없다.

File, Edit, Tools차림표의 다른 작용들은 New작용과 아주 비슷하다.

Show Grid는 절환(toggle)작용이다. 이것은 차림표에서 검사표식으로 표시되고 도구띠에서 절환단추로서 실현된다. 작용이 on일 때 Spreadsheet부분품은 살창을 현시한다. 작용을 Spreadsheet부분품의 기정값으로 초기화하여 그것들을 기동시에 동기시킨다. 그다음 Show Grid작용의 toggled(bool)신호를 QTable로부터 계승하는 Spreadsheet부분품의 setShowGrid(bool)처리부에 련결한다. 일단 이 작용이 차림표 혹은 도구띠에 추가되면 사용자는 살창의 on/off를 절환할수 있다.

Show Grid와 Auto-recalculate작용들은 독립적인 절환작용들이다. 또한 QAction은 QActionGroup파생클라스를 통하여 호상 배타적인 작용들을 제공한다.

void MainWindow::createMenus(){

fileMenu = new QPopupMenu(this);

newAct→addTo(fileMenu); openAct→addTo(fileMenu);

saveAct→addTo(fileMenu); saveAsAct→addTo(fileMenu);

fileMenu→insertSeparator(); exitAct→addTo(fileMenu);

for (int i = 0; i < MaxRecentFiles; ++i)

recentFileIds[i] = -1;

editMenu = new QPopupMenu(this);

cutAct→addTo(editMenu); copyAct→addTo(editMenu);

pasteAct→addTo(editMenu); deleteAct→addTo(editMenu);

selectSubMenu = new QPopupMenu(this);

selectRowAct→addTo(selectSubMenu); selectColumnAct→addTo(selectSubMenu);

selectAllAct→addTo(selectSubMenu);

editMenu→insertItem(tr("&Select"), selectSubMenu);

editMenu→insertSeparator();

findAct→addTo(editMenu); goToCellAct→addTo(editMenu);

toolsMenu = new QPopupMenu(this);

recalculateAct→addTo(toolsMenu); sortAct→addTo(toolsMenu);

optionsMenu = new QPopupMenu(this);

showGridAct→addTo(optionsMenu); autoRecalcAct→addTo(optionsMenu);

helpMenu = new QPopupMenu(this);

aboutAct→addTo(helpMenu); aboutQtAct→addTo(helpMenu);

menuBar()→insertItem(tr("&File"), fileMenu);

menuBar()→insertItem(tr("&Edit"), editMenu);

menuBar()→insertItem(tr("&Tools"), toolsMenu);

menuBar()→insertItem(tr("&Options"), optionsMenu);

menuBar()→insertSeparator();

menuBar()→insertItem(tr("&Help"), helpMenu);

}

Qt에서 모든 차림표는 QPopupMenu의 실례들이다. File차림표를 창조한 다음 거기에 New, Open, Save, Save As, Exit작용들을 추가한다. 분리선을 추가하여 밀접히 련관된 항목들을 모두 시각적으로 묶는다. for순환을 리용하여 recentFilesIds배렬을 초기화한다.

Edit차림표는 하나의 보조차림표를 포함한다. 보조차림표는 그것이 속하는 차림표처럼 QPopupMenu이다. 단순히 this를 부모로 가지는 보조차림표를 창조하여 그것을 표시하려는 Edit차림표에 삽입한다.

류사한 방법으로 Tools, Options, Help차림표들을 만들어 모든 차림표를 차림표띠에 삽입한다. QMainWindow::menuBar()함수는 QMenuBar의 지적자를 돌려준다. Options과 Help차림표사이에 분리선을 삽입한다. Motif형식에서 분리선은 Help차림표를 오른쪽에 배치하며 다른 형식들에서 분리선은 무시된다.

도구띠의 창조는 차림표창조와 아주 비슷하다.

void MainWindow::createToolBars(){

fileToolBar = new QToolBar(tr("File"), this);

newAct→addTo(fileToolBar); openAct→addTo(fileToolBar);

saveAct→addTo(fileToolBar);

editToolBar = new QToolBar(tr("Edit"), this);

cutAct→addTo(editToolBar); copyAct→addTo(editToolBar);

pasteAct→addTo(editToolBar); editToolBar→addSeparator();

findAct→addTo(editToolBar); goToCellAct→addTo(editToolBar);

}

File도구띠와 Edit도구띠를 창조한다. 튀여나오기차림표처럼 도구띠는 분리선을 가질수 있다.

이제는 차림표와 도구띠를 만들었으므로 문맥차림표를 추가하여 대면부를 완성한다.

void MainWindow::contextMenuEvent(QContextMenuEvent *event){

QPopupMenu contextMenu(this);

cutAct→addTo(&contextMenu); copyAct→addTo(&contextMenu);

pasteAct→addTo(&contextMenu);

contextMenu.exec(event→globalPos());

}

사용자가 오른쪽 마우스단추를 찰칵할 때(혹은 일부 건반우에 있는 Menu건을 누를 때) 《문맥차림표》사건이 창문부분품에 전송된다. QWidget::contextMenuEvent()함수를 재정의하여 이 사건에 응답할수 있으며 현재의 마우스지시자위치에 문맥차림표를 펼친다.

대표적으로 File차림표의 실현과정은 다음과 같다.

void MainWindow::newFile() {

if (maybeSave()) {

spreadsheet→clear();

setCurrentFile("");

}

}

newFile()처리부는 사용자가 File|New차림표를 찰칵하거나 New도구띠단추를 찰칵할 때 호출된다. maybeSave()비공개함수는 보관안된 변경이 있으면 사용자에게 "Do you want to save your changes?"라고 묻는다. 사용자가 Yes 혹은 No(문서를 보관할 때 Yes)를 선택하면 true를 돌려주고 사용자가 Cancel을 선택하면 false를 돌려준다. setCurrentFile()비공개함수는 새로 만든 화일이 제목이 없으므로 창문제목을 기정제목으로 설정한다.

bool MainWindow::maybeSave(){

if (modified) {

int ret = QMessageBox::warning(this, tr("Spreadsheet"),

tr("The document has been modified.\n" "Do you want to save your changes?"),

QMessageBox::Yes | QMessageBox::Default, QMessageBox::No,

QMessageBox::Cancel | QMessageBox::Escape);

if (ret == QMessageBox::Yes)

return save();

else if (ret == QMessageBox::Cancel)

return false;

}

return true;

}

통보창은 Yes, No, Cancel단추를 가진다. QMessageBox::Default는 Yes를 기정단추로 만든다. QMessageBox::Escape는 Esc건을 Cancel과 같은 의미로 만들어준다.

void MainWindow::open() {

if (maybeSave()) {

QString fileName = QFileDialog::getOpenFileName(".", fileFilters, this);

if (!fileName.isEmpty())

loadFile(fileName);

}

}

open()처리부는 File|Open에 대응된다. newFile()처럼 open()처리부는 우선 maybeSave()를 호출하여 보관하지 않은 변경을 조종한다. 그다음 정적편의함수 QFileDialog::getOpenFileName()에 의하여 화일이름을 얻는다. 이 함수는 화일대화창을 펼치고 사용자가 화일을 선택하면 화일이름(혹은 사용자가 Cancel을 찰칵하면 빈 문자렬)을 돌려준다.

getOpenFileName()함수에 3개의 인수를 준다. 첫째 인수는 기동하려는 등록부, 이 경우에 현재 등록부를 함수에 알린다. 둘째 인수 fileFilters는 화일려과기들을 지정한다.

화일려과기는 화일형이름과 확장자로 이루어진다. MainWindow구성자에서 fileFilters는 다음과 같이 초기화된다.

fileFilters = tr("Spreadsheet files (*.sp)");

끝으로 getOpenFileName()의 셋째 인수는 펼쳐지는 QFileDialog가 기본창문의 자식으로 되여야 한다는것을 지정한다.

부모-자식관계는 대화창에서 다른 창문부분품에서와 같은 의미가 아니다. 대화창은 늘 제일 웃준위 창문부분품(자체가 창문)이지만 그것이 부모를 가지면 기정으로 부모의 우에 중심에 배치된다. 또한 자식대화창은 부모의 과제띠항목을 공유한다.

void MainWindow::loadFile(const QString &fileName) {

if (spreadsheet→readFile(fileName)) {

setCurrentFile(fileName);

statusBar()→message(tr("File loaded"), 2000);

} else

statusBar()→message(tr("Loading canceled"), 2000);

}

loadFile()비공개함수는 화일을 적재하기 위하여 open()에서 호출된다. 최근에 연 화일들을 적재하는데 같은 기능이 필요하므로 그것을 독립적인 함수로 만든다.

Spreadsheet::readFile()에 의하여 디스크로부터 화일을 읽어들인다. 적재에서 성공하면 setCurrentFile()을 호출하여 창문의 제목을 갱신한다.

그렇지 않으면 Spreadsheet::loadFile()은 사용자에게 통보창을 통하여 문제점에 대하여 미리 통지한다. 일반적으로 저준위부분품들이 오유에 대한 정확한 내용을 제공할수 있으므로 오유통보문을 내게 하는것이 좋다.

두 경우에 2 000㎳(2s)동안 상태띠에 통보문을 현시하여 응용프로그람이 수행하는 일을 사용자가 알수 있게 한다.

bool MainWindow::save() {

if (curFile.isEmpty()) {

return saveAs();

} else {

saveFile(curFile);

return true;

}

}

void MainWindow::saveFile(const QString &fileName) {

if (spreadsheet→writeFile(fileName)) {

setCurrentFile(fileName);

statusBar()→message(tr("File saved"), 2 000);

} else

statusBar()→message(tr("Saving canceled"), 2 000);

}

save()처리부는 File|Save에 대응된다. 화일이 이전에 열렸거나 이미 보관되였기때문에 화일에 이미 이름이 있으면 save()는 그 이름으로 saveFile()를 호출하고 그렇지 않으면 단순히 saveAs()를 호출한다.

bool MainWindow::saveAs() {

QString fileName = QFileDialog::getSaveFileName(".", fileFilters, this);

if (fileName.isEmpty())

return false;

if (QFile::exists(fileName)) {

int ret = QMessageBox::warning(this, tr("Spreadsheet"), tr("File %1 already exists. \n" "Do you want to overwrite it?")

.arg(QDir::convertSeparators(fileName)),

QMessageBox::Yes | QMessageBox::Default,

QMessageBox::No | QMessageBox::Escape);

if (ret == QMessageBox::No)

return true;

}

if (!fileName.isEmpty())

saveFile(fileName);

return true;

}

saveAs()처리부는 File|Save As에 대응된다. QFileDialog::getSaveFileName()를 호출하여 사용자로부터 화일이름을 얻는다. 사용자가 Cancel을 찰칵하면 false를 돌려주는데 이것은 maybeSave()까지 전달된다. 그렇지 않으면 돌아온 화일이름은 새로운 이름이거나 현존 화일의 이름이다. 현존 화일의 경우에는 QMessageBox::warning()를 호출하여 통보창을 현시한다.

통보창에 넘긴 본문은 다음과 같다.

tr("File %1 already exists\n"

"Do you want to override it?")

.arg(QDir::convertSeparators(fileName))

QString::arg()함수는 "%n"파라메터를 그 인수로 바꾸고 결과문자렬을 돌려준다. 례를 들면 화일이름이 C:\tab04.sp이면 우의 코드는 다음과 같다.

"File C:\\tab04.sp already exists.\n"

"Do you want to override it?"

이것은 응용프로그람이 다른 언어로 번역되지 않는것을 전제로 하고있다.

QDir::convertSeparators()호출은 Qt가 이식가능한 등록부분리기호로 사용하는 사선들을 가동환경에 고유한 분리기호(Unix와 Mac OS X에서 '/', Windows에서 '\' on)로 변환한다.

void MainWindow::closeEvent(QCloseEvent *event) {

if (maybeSave()) {

writeSettings();

event→accept();

} else

event→ignore();

}

사용자가 File|Exit를 찰칵하거나 창문제목띠의 ×를 찰칵할 때 QWidget::close()처리부가 호출된다. 이것은 close사건을 창문부분품에 송신한다. QWidget::closeEvent()를 재정의함으로써 기본창문을 닫으려는 시도를 받아들이고 창문을 닫으려고 하는가 아닌가를 결정할수 있다.

보관하지 않은 변경내용이 있는데 사용자가 Cancel을 선택하면 그 사건을 《무시》하고 창문은 그대로 남아있다. 그렇지 않으면 사건을 받아들이고 Qt에서는 창문을 닫으며 응용프로그람을 완료한다.

void MainWindow::setCurrentFile(const QString &fileName) {

curFile = fileName;

modLabel→clear();

modified = false;

if (curFile.isEmpty()) {

setCaption(tr("Spreadsheet"));

} else {

setCaption(tr("%1 -%2").arg(strippedName(curFile)).arg(tr("Spreadsheet")));

recentFiles.remove(curFile);

recentFiles.push_front(curFile);

updateRecentFileItems();

}

}

QString MainWindow::strippedName(const QString &fullFileName){

return QFileInfo(fullFileName).fileName();

}

setCurrentFile()에서는 편집중에 있는 화일의 이름을 보관하는 curFile비공개변수를 설정하고 MOD상태지시자를 지우고 제목을 갱신한다. 두개의 %n파라메터에 대하여 arg()를 사용한다. arg()의 첫 호출은 "%1"로 교체되고 둘째 호출은 "%2"로 교체된다.

setCaption(strippedName(curFile) + tr(" -Spreadsheet"));와 같이 쓰는것이 더 좋지만 arg()를 사용하면 번역기에 유연성을 준다. strippedName()에 의하여 화일의 경로를 삭제하고 화일이름을 사용자에게 편리하게 만든다.

화일이름이 있으면 응용프로그람의 최근에 연 화일목록인 recentFiles를 갱신한다. remove()를 호출하여 목록에서 화일이름을 삭제한 다음 push_front()를 호출하여 화일이름을 첫 항목으로서 추가한다. remove()의 호출은 무엇보다 먼저 중복을 피하는데 필요하다. 목록을 갱신한 후에 비공개함수 updateRecentFileItems()를 호출하여 File차림표전부를 갱신한다.

recentFiles변수는 QStringList형(QString의 목록)이다.

void MainWindow::updateRecentFileItems(){

while ((int)recentFiles.size() > MaxRecentFiles)

recentFiles.pop_back();

for (int i = 0; i < (int)recentFiles.size(); ++i) {

QString text = tr("&%1 %2").arg(i + 1).arg(strippedName(recentFiles[i]));

if (recentFileIds[i] == –1) {

if (i == 0)

fileMenu→insertSeparator(fileMenu→count() – 2);

recentFileIds[i] = fileMenu→insertItem(text, this, SLOT(openRecentFile(int)), 0, –1, fileMenu→count() – 2);

fileMenu→setItemParameter(recentFileIds[i], i);

} else

fileMenu→changeItem(recentFileIds[i], text);

}

}

updateRecentFileItems()비공개함수는 최근에 연 화일들의 차림표항목을 갱신하기 위하여 호출된다. recentFiles목록에 허용된것보다 항목이 많지 않는가(MaxRecentFiles, mainwindow.h에서 5로 정의되였다.)를 확인하고 목록의 끝으로부터 남는 항목들을 삭제한다.

그다음 매개 항목들에 대하여 새로운 차림표항목을 창조하거나 혹은 존재하는 경우 현존 항목을 재리용한다. 차림표항목을 처음으로 창조할 때 또한 분리선을 삽입한다. 이것을 createMenus()가 아니라 여기서 수행하여 한 행에 두개의 분리선을 절대로 현시하지 않도록 한다. setItemParameter()호출을 간단히 설명한다.

이것은 updateRecentFileItems()에서 항목들을 창조하지만 절대로 항목들을 삭제하지 않는것처럼 보일수 있다. 그것은 최근에 연 화일목록이 대화(Session)기간에 절대로 줄어들지 않는다고 가정할수 있기때문이다.

QPopupMenu::insertItem()함수는 아래와 같은 형식을 가진다.

fileMenu→insertItem(text, receiver, slot, accelerator, id, index);

text는 차림표에 현시된 본문이다. strippedName()을 사용하여 화일이름으로부터 경로를 삭제한다. 완전화일이름을 유지할수 있지만 그렇게 되면 File차림표가 너무 길어지게 된다. 완전한 화일차림표를 표시하려면 보조차림표에 최근에 연 화일들을 넣어야 한다.

receiver와 slot파라메터들은 사용자가 항목을 선택할 때 호출되여야 할 처리부를 지정한다. 실례에서는 MainWindow의 openRecentFile(int)처리부에 련결한다.

accelerator와 id에는 차림표항목에 지름건이 없으며 자동적으로 생성된 ID를 가진다는것을 의미하는 기정값들을 넘긴다. 생성된 ID를 recentFileIds배렬에 보관하여 후에 항목들을 호출할수 있다.

index는 항목을 삽입하려고 하는 위치이다. 값 fileMenu→count()–2를 넘김으로써 Exit항목의 분리선우에 그것을 삽입한다.

void MainWindow::openRecentFile(int param){

if (maybeSave())

loadFile(recentFiles[param]);

}

openRecentFile()처리부는 많은 곳에서 호출되는 처리부이다. 이 처리부는 File차림표로부터 최근에 연 화일이 선택될 때 호출된다. int파라메터는 setItemParameter()로 초기에 설정한 값이다. recentFiles목록에 대한 첨수로서 그것들을 사용하는 방법으로 값들을 선택하였다.

### 3. 상태띠의 설정

표준상태에서 상태띠는 3개의 지시자(indicator) 즉 현재 세포의 위치, 현재 세포의 식, MOD로 이루어진다. 또한 상태띠는 상태암시와 다른 림시통보문들을 현시하는데 쓰인다.

MainWindow구성자는 createStatusBar()를 호출하여 상태띠를 설정한다.

void MainWindow::createStatusBar(){

locationLabel = new QLabel(" W999 ", this);

locationLabel→setAlignment(AlignHCenter);

locationLabel→setMinimumSize(locationLabel→sizeHint());

formulaLabel = new QLabel(this);

modLabel = new QLabel(tr(" MOD "), this);

modLabel→setAlignment(AlignHCenter);

modLabel→setMinimumSize(modLabel→sizeHint()); modLabel→clear();

statusBar()→addWidget(locationLabel); statusBar()→addWidget(formulaLabel, 1);

statusBar()→addWidget(modLabel);

connect(spreadsheet, SIGNAL(currentChanged(int, int)), this, SLOT(updateCellIndicators()));

connect(spreadsheet, SIGNAL(modified()), this, SLOT(spreadsheetModified()));

updateCellIndicators();
}

QMainWindow::statusBar()함수는 상태띠의 지적자를 돌려준다.(상태띠는 statusBar()가 처음으로 호출될 때 창조된다.) 상태지시자는 필요할 때마다 본문이 변하는 QLabel이다. QLabel들을 구성할 때 this를 부모로서 넘기지만 QStatusBar::addWidget()가 그것들의 부모자식관계를 자동적으로 재설정하여 자식들을 만드므로 실제로 문제는 없다.

QStatusBar가 지시자창문부분품들을 배치할 때 QWidget::sizeHint()에 의해 주어진 매개 창문부분품의 리상적인 크기를 고려하여 사용가능한 공간을 채우도록 창문부분품들을 늘인다. 창문부분품의 리상크기는 창문부분품의 내용에 따라 달라진다. 위치와 MOD지시자들의 크기가 끊임없이 변하는것을 피하기 위하여 그것들의 최소크기를 매개 지시자에서 가능한 최대본문을 다 포함하는 폭("W999"와 "MOD")으로 설정한다. 또한 그것들의 배치를 AlignHCenter로 설정하여 본문이 수평으로 중심에 놓이도록 한다.

함수의 끝부근에서 Spreadsheet의 2개 신호를 MainWindow의 처리부 update CellIndicators()와 spreadsheetModified()에 련결한다.

void MainWindow::updateCellIndicators() {

locationLabel→setText(spreadsheet→currentLocation());

formulaLabel→setText(" " + spreadsheet→currentFormula());

}

updateCellIndicator()처리부는 세포위치와 세포식, 지시자들을 갱신한다. 이것은 사용자가 세포마우스지시자를 새로운 세포로 이행할 때마다 호출된다. 또한 그 처리부는 createStatusBar()의 끝에서 보통의 함수로 사용되여 지시자들을 초기화한다. 이것은 Spreadsheet가 기동시에 currentChanged()신호를 발생하지 않으므로 필요하다.

void MainWindow::spreadsheetModified() {

modLabel→setText(tr("MOD")); modified = true; updateCellIndicators();

}

spreadsheetModified()처리부는 3개의 지시자를 모두 갱신하여 사건의 현재상태를 반영하고 변경된 변수를 true로 설정한다.(File차림표를 실현할 때 modified변수를 사용하여 보관하지 않은 변경이 있는가 결정하였다.)

## 제4절. 사용자정의창문

사용자정의창문부분품은 Qt의 현존 창문부분품들의 파생클라스를 만들거나 QWidget의 파생클라스를 직접 만들어서 창조할수 있다.

### 1. 창문부분품들의 사용자정의

QSpinBox는 오직 10진옹근수만 유지하지만 그 파생클라스를 만들어 16진수값들을 받아들이고 표시하는것은 아주 간단하다.

HexSpinBox는 QSpinBox로부터 대부분의 기능을 계승한다. 이 클라스는 전형적인 구성자를 제공하고 QSpinBox로부터 2개의 가상함수를 실현한다. 클라스가 자체의 신호와 처리부를 정의하지 않으므로 Q_OBJECT마크로가 필요없다.

#include <qvalidator.h>

#include "hexspinbox.h"

HexSpinBox::HexSpinBox(QWidget *parent, const char *name) : QSpinBox(parent, name) {

QRegExp regExp("[0-9A-Fa-f]+");

setValidator(new QRegExpValidator(regExp, this));

setRange(0, 255);

}

사용자는 스핀칸의 올리, 내리화살표를 찰칵하거나 스핀칸의 행편집기에 값을 입력하여 현재 값을 수정할수 있다. 값을 직접 입력하는 경우 정확한 16진수를 입력하도록 제한하려고 한다. 그러기 위하여 범위 0～9, A～F, a～f로부터 하나이상의 문자들을 받아들이는 QRegExpValidator를 리용한다. 또한 기정범위를 0～255(0x00～0xFF)로 설정한다. 이것은 QSpinBox의 기정값 0～99보다 16진수 스핀칸에 더 적합하다.

QString HexSpinBox::mapValueToText(int value){

return QString::number(value, 16).upper();

}

mapValueToText()함수는 옹근수값을 문자렬로 변환한다. QSpinBox는 이 함수를 호출하여 사용자가 스핀칸의 올리 혹은 내리화살표를 누를 때 스핀칸의 편집기부분을 갱신한다. 둘째 인수로서 16을 가지는 정적함수 QString::number()를 리용하여 소문자 16진수로 값을 변환하고 결과에 대하여 QString::upper()를 호출하여 그것을 대문자로 만든다.

int HexSpinBox::mapTextToValue(bool *ok) { return text().toInt(ok, 16); }

mapTextToValue()함수는 문자렬로부터 옹근수값에로의 역변환을 진행한다. 사용자가 스핀(spin)칸의 편집기부분에 값을 입력하고 Enter건을 누르면 이 함수가 QSpinBox에 의해 호출된다. QString::toInt()함수에 의하여 현재 본문(QSpinBox::text()로부터 돌아온다.)을 16진옹근수값으로 변환한다.

변환이 성공하면 toInt()는 *ok를 true로 설정하고 그렇지 않으면 false로 설정한다.

### 2. QWidget의 파생클라스만들기

대부분의 사용자정의창문부분품들은 그것이 Qt내부창문부분품이든 HexSpinBox와 같은 사용자정의창문부분품이든 순수 현존 창문부분품들의 결합이다. 현존 창문부분품들을 결합하여 구축하는 사용자정의창문부분품들은 보통 Qt Designer로 개발할수 있다. 즉

·Widget형판을 사용하여 새 대면형식창을 작성한다.

·대면형식창에 필요한 창문부분품들을 추가하고 배치한다.

·신호와 처리부련결을 설정하고 .ui.h화일 혹은 파생클라스에 필요한 코드를 추가하여 요구되는 동작을 제공한다.

이것은 완전히 코드로도 수행할수 있다. 어떤 방법을 취하든간에 결과클라스는 QWidget로부터 직접 계승된다.

창문부분품이 자체의 신호와 처리부를 가지지 않고 가상함수들을 재정의하지 않으면 파생클라스없이 현존 창문부분품들을 수집하여 창문부분품을 간단히 조립할수도 있다. 그러나 QHBox의 파생클라스를 간단히 만들고 파생클라스의 구성자에서 QSpinBox와 QSlider를 창조하였다.

Qt의 어떤 창문부분품도 현재의 과제에 적합하지 않을 때와 현존 창문부분품들을 결합하거나 적용하여 요구되는 결과를 얻는 방법이 없을 때에는 요구되는 창문부분품을 창조한다. 이것은 QWidget의 파생클라스를 만들고 몇가지 사건처리함수들을 재정의하여 창문부분품을 그리고 마우스찰칵에 응답하게 하는 방법으로 달성한다. 이 수법은 완전히 자유롭게 창문부분품의 표현과 동작을 정의하고 조종하게 한다. QLabel, QPushButton, QTable과 같은 Qt의 기본창문부분품들은 이렇게 실현된다. Qt에 그것들이 존재하지 않으면 총체적으로는 가동환경에 의존하지 않는 방법으로 QWidget가 제공하는 공개함수들을 리용하여 자체로 창조할수 있다.

이러한 수법으로 사용자정의창문부분품을 쓰는 방법을 보여주기 위하여 IconEditor창문부분품을 창조한다. IconEditor는 그림기호편집프로그람에서 사용할수 있는 창문부분품이다.

IconEditor는 QWidget로부터 3개의 보호함수를 재정의하고 여러개의 비공개함수와 변수들을 가진다. 3개의 비공개변수는 3가지 속성의 값들을 보관한다.

실현화일은 #include지령과 IconEditor의 구성자로 시작된다.

#include <qpainter.h>

#include "iconeditor.h"

IconEditor::IconEditor(QWidget *parent, const char *name): QWidget(parent, name, WStaticContents) {

setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);

curColor = black;

zoom = 8;

image.create(16, 16, 32); image.fill(qRgba(0, 0, 0, 0));

image.setAlphaBuffer(true);

}

구성자는 setSizePolicy()호출과 WStaticContents기발과 같은 미묘한 점들을 가진다.

확대곁수는 8로 설정되고 이것은 그림기호안의 매개 화소가 8×8인 바른4각형으로 표시된다는것을 의미한다. 펜색갈은 흑색으로 설정되고 흑색기호는 Qt클라스(QObject의 기초클라스)에서 미리 정의된 값이다.

그림기호자료는 image성원변수에 보관되고 setIconImage()와 iconImage()함수를 통하여 호출될수 있다. 일반적으로 그림기호편집프로그람은 그림기호화일을 열 때 setIconImage()를, 사용자가 그림기호화일을 닫으려고 할 때 그림기호를 얻기 위하여 iconImage()를 호출한다.

image변수는 QImage형이다. 그것을 16×16화소와 32bit깊이로 초기화하고 화상자료를 지우며 알파완충기를 허용한다.

QImage클라스는 하드웨어에 의존하지 않는 형식으로 화상을 보관한다. 이 클라스는1bit, 8bit 혹은 32bit깊이를 사용하도록 설정할수 있다. 32bit깊이의 화상은 화소의 적색, 록색, 청색요소에 각각 8bit를 리용한다. 나머지 8bit는 화소의 알파요소 즉 불투명도를 보관한다. 례를 들면 순수한 적색, 록색, 청색과 알파요소는 값 255, 0, 0과 255를 가진다. Qt에서 이 색은 QRgb red = qRgba(255, 0, 0, 255);과 같이 지정되거나 QRgb red = qRgb(255, 0, 0);와 같이 지정될수 있다.

QRgb는 unsigned int의 형정의이고 qRgb()와 qRgba()는 32bit옹근수값으로 인수들을 결합하는 inline함수들이다. 또한 다음과 같이 쓸수도 있다.

QRgb red = 0xFFFF0000;

여기서 첫 FF는 알파요소에 대응하고 둘째 FF는 적색요소에 대응한다. IconEditor구성자에서는 알파요소로서 0을 리용하여 투명색으로 QImage를 채운다.

Qt는 색을 보관하는 2가지 형 즉 QRgb와 QColor를 제공한다. QRgb가 32bit화소자료를 보관하기 위해 QImage에서 사용된 형정의이지만 QColor는 사용가능한 수많은 함수들을 가지는 클라스로서 Qt에서 색을 보관하는데 널리 사용된다. IconEditor창문부분품에서는 QImage를 론할 때 QRgb만 사용하며 penColor속성을 비롯하여 그밖의 모든것에는 QColor를 사용한다.

QSize IconEditor::sizeHint() const {

QSize size = zoom * image.size();

if (zoom >= 3)

size += QSize(1, 1);

return size;

}

sizeHint()함수는 QWidget로부터 재정의되고 창문부분품의 리상크기를 돌려준다. 여기서는 화상크기에 zoom곁수를 곱하고 zoom곁수가 3이상이면 각 방향으로 여유로서 1화소를 더하여 살창을 조절한다.(zoom곁수가 2나 1이면 그림기호의 화소와 같은 칸으로 되므로 살창은 표시되지 않는다.) 대체로 창문부분품의 크기암시는 배치체계와 결합되여 쓰일수 있다. Qt의 배치관리자들은 대면형식창의 자식창문부분품들을 배치할 때 창문부분품의 크기암시를 최대한 고려하려고 한다. IconEditor가 좋은 배치도구로 되자면 그것이 신용할만한 크기암시를 알려주어야 한다.

크기암시와 함께 창문부분품들을 늘이겠는가 줄이겠는가를 배치체계에 알리는 크기방략을 가진다. 구성자에서 수평과 수직크기방략으로서 QSizePolicy::Minimum을 리용하여 setSizePolicy()를 호출함으로써 창문부분품의 크기암시가 실제로 그 최소크기이라는것을 배치관리자에 알려야 한다. 다시말하여 창문부분품은 필요하다면 그 크기를 늘일수 있지만 크기암시아래로 줄일수 없다. 이것은 창문부분품의 sizePolicy속성을 설정하여 Qt Designer에서 거절할수 있다.

void IconEditor::setPenColor(const QColor &newColor) { curColor = newColor; }

setPenColor()함수는 현재 펜색을 설정한다. 그 색은 새로 그리는 화소에 사용될수 있다.

void IconEditor::setIconImage(const QImage &newImage){

if (newImage != image) {

image = newImage.convertDepth(32);

image.detach();

update(); updateGeometry();

}

}

setIconImage()함수는 편집하려는 화상을 설정한다. 32bit화상이 아닌 경우에는 convertDepth()를 호출하여 32bit화상으로 만든다. 코드의 모든 곳에서 화상자료가 32bit QRgb값으로 보관되는것으로 가정한다.

또한 detach()를 호출하여 화상에 보관된 자료의 깊이사본을 얻는다. 이것은 화상자료가 ROM에 보관될수 있기때문에 필요하다. QImage는 정확히 요구될 때에만 화상을 복사하여 시간과 기억기를 절약하려고 한다. 이러한 최량화를 명시적공유라고 한다.

image변수를 설정한 후에 QWidget::update()를 호출하여 새 화상으로 창문부분품을 다시 그리게 한다. 다음에 QWidget::updateGeometry()를 호출하여 크기암시가 달라진 창문부분품을 포함한다는것을 배치관리자에 알린다. 그때 배치관리자는 자동적으로 새로운 크기암시를 받아들인다.

void IconEditor::setZoomFactor(int newZoom){

if (newZoom < 1)

newZoom = 1;

if (newZoom != zoom) {

zoom = newZoom;

update(); updateGeometry();

}

}

setZoomFactor()함수는 화상의 zoom곁수를 설정한다. 후에 0에 의한 나누기를 방지하기 위하여 1아래의 값은 수정한다. update()와 updateGeometry()를 호출하여 창문부분품을 다시 그리고 크기암시변경에 대하여 배치관리자에 통지한다.

penColor(), iconImage(), zoomFactor()함수들은 머리부화일에서 inline함수들로 실현된다.

paintEvent()함수는 IconEditor의 가장 중요한 함수로서 창문부분품이 다시 그려질 때마다 호출된다. QWidget의 기정적으로 아무 일도 하지 않고 창문부분품은 비여있다.

그리기사건이 발생하고 paintEvent()가 호출되는 경우는 다음과 같다.

·창문부분품이 처음으로 표시될 때 체계는 자동적으로 그리기사건을 생성하여 창문부분품을 자체로 그리게 한다.

·창문부분품의 크기가 조절될 때 체계는 자동적으로 그리기사건을 생성한다.

·창문부분품이 다른 창문에 의하여 가리워졌다가 다시 나타나면(창문체계가 그 구역을 보관하지 않으면) 가리워졌던 구역에 대하여 그리기사건이 발생된다.

또한 QWidget::update()나 QWidget::repaint()를 호출하여 그리기사건을 강제로 발생시킬수도 있다. 이 두 함수들사이의 차이는 repaint()는 즉시 재그리기를 진행하지만 update()는 단순히 Qt가 다음에 사건들을 처리할 때 그리기사건을 발생한다는데 있다.(두 함수는 창문부분품이 화면에 표시되지 않으면 아무 일도 하지 않는다.) update()가 여러번 호출되면 Qt는 깜빡거림을 피하기 위하여 그리기사건들을 하나의 그리기사건으로 압축한다. IconEditor에서는 늘 update()을 사용한다.

void IconEditor::paintEvent(QPaintEvent *){

QPainter painter(this);

if (zoom >= 3) {

painter.setPen(colorGroup().foreground());

for (int i = 0; i <= image.width(); ++i)

painter.drawLine(zoom * i, 0, zoom * i, zoom * image.height());

for (int j = 0; j <= image.height(); ++j)

painter.drawLine(0, zoom * j, zoom * image.width(), zoom * j);

}

for (int i = 0; i < image.width(); ++i) {

for (int j = 0; j < image.height(); ++j)

drawImagePixel(&painter, i, j);

}

}

창문부분품에 QPainter객체를 창조한다. zoom곁수가 3이상이면 QPainter::drawLine()함수에 의하여 살창을 구성하는 수평 및 수직선들을 그린다.

QPainter::drawLine()호출은 다음의 문법을 가지고있다.

painter.drawLine(x1, y1, x2, y2);

여기서 (x1, y1)는 직선의 한 끝의 위치, (x2, y2)는 다른 끝의 위치이다. 또한 4개의 int대신에 2개의 QPoint를 가지는 다중정의판의 함수가 있다.

Qt창문부분품의 왼쪽웃구석의 화소는 위치 (0, 0)에 배치되고 오른쪽아래구석의 화소는 (width()– 1, height()– 1)에 배치된다. 이것은 관례적인 데카르트자리표계와 비슷하지만 y축의 방향이 바뀌고 프로그람작성에서 많이 사용된다. 이행, 비례, 회전, 자름과 같은 변환을 리용하여 QPainter의 자리표계를 변환할수도 있다.

QPainter에 대하여 drawLine()를 호출하기 전에 setPen()에 의하여 선의 색을 설정한다. 흑색이나 재색과 같은 색을 코드로 작성할수 있으나 창문부분품의 조색판을 사용하는것이 더 좋은 수법이다.

매개 창문부분품에는 사용할 색을 지정하는 조색판이 구비된다. 례를 들면 창문부분품들의 배경색(보통 밝은 재색)을 위한 조색판항목과 배경우에 표시되는 본문색(보통 흑색)을 위한 조색판항목이 있다. 기정으로 창문부분품의 조색판은 창문체계의 색구조를 받아들인다. 조색판의 색을 리용하여 IconEditor가 사용자의 선택을 고려하도록 한다.

창문부분품의 조색판은 3개의 색묶음 즉 능동, 비능동 및 금지로 이루어진다. 사용하려는 색묶음은 창문부분품의 현재 상태에 의존한다.

·능동색묶음(active color group)은 현재 능동인 창문안에 있는 창문부분품들에서 사용된다.

·비능동색묶음(inactive color group)은 다른 창문들안의 창문부분품들에서 사용된다.

·금지색묶음(disable color group)은 임의의 창문의 금지된 창문부분품들에서 사용된다.

QWidget::palette()함수는 창문부분품의 조색판을 QPalette객체로서 돌려준다. 색묶음은 QPalette의 active(), inactive(), disabled()함수들을 통하여 유효로 되며 QColorGroup형이다. 편리상 QWidget::colorGroup()는 창문부분품의 현재 상태에 대한 정확한 색묶음을 돌려주므로 간혹 조색판을 직접 호출해야 한다.

paintEvent()함수는 화상자체를 그리는것으로 끝난다. 이때 IconEditor::draw ImagePixel()함수에 의하여 그림기호의 매개 화소를 색칠한 바른4각형을 그린다.

void IconEditor::drawImagePixel(QPainter *painter, int i, int j){

QColor color;

QRgb rgb = image.pixel(i, j);

if (qAlpha(rgb) == 0)

color = colorGroup().base();

else

color.setRgb(rgb);

if (zoom >= 3) {

painter→fillRect(zoom * i + 1, zoom * j + 1, zoom -1, zoom -1, color);

} else

painter→fillRect(zoom * i, zoom * j, zoom, zoom, color);

}

drawImagePixel()함수는 QPainter에 의하여 확대된 화소를 그린다. i와 j파라메터는 창문부분품이 아니라 QImage의 화소자리표이다.(zoom곁수가 1이면 두개 자리표계는 정확히 일치한다.) 화소가 투명이면(알파요소가 0이면) 현재색묶음의 《기준》색(일반적으로 백색)으로 화소를 그리고 그렇지 않으면 화상안의 화소색을 리용한다. 그다음 QPainter::fillRect()을 호출하여 색으로 채운 바른4각형을 그린다. 살창이 표시되면 바른4각형을 량방향으로 1화소씩 감소하여 살창밖에 그리는것을 막는다.

QPainter::fillRect()호출은 다음의 문법을 가진다.

painter→fillRect(x, y, w, h, brush);

여기서 (x, y)는 직4각형의 왼쪽웃구석의 위치, w×h는 직4각형의 크기이고 brush는 채우려는 색과 사용하려는 도색견본을 지정한다.

void IconEditor::mousePressEvent(QMouseEvent *event){

if (event→button() == LeftButton)

setImagePixel(event→pos(), true);

else if (event→button() == RightButton)

setImagePixel(event→pos(), false);

}

사용자가 마우스단추를 누를 때 체계는 《마우스누르기》사건을 생성한다. QWidget::mousePressEvent()를 재정의하여 사건에 응답할수 있으며 마우스지시자밑의 화상화소를 설정하거나 지울수 있다.

사용자가 왼쪽 마우스단추를 찰칵하면 둘째 인수를 true로 하여 비공개함수setImagePixel()를 호출함으로써 화소를 현재펜색으로 설정한다. 사용자가 오른쪽마우스단추를 찰칵하면 역시 setImagePixel()를 호출하지만 false를 넘기여 화소를 지운다.

void IconEditor::mouseMoveEvent(QMouseEvent *event){

if (event→state() & LeftButton)

setImagePixel(event→pos(), true);

else if (event→state() & RightButton)

setImagePixel(event→pos(), false);

}

mouseMoveEvent()는 《마우스이동》사건들을 처리한다. 기정으로 이 사건들은 사용자가 단추를 누르고있을 때에만 생성된다. QWidget::setMouseTracking()를 호출하여 이 동작을 변경할수 있으나 이 실례에서는 그럴 필요가 없다.

왼쪽 혹은 오른쪽 마우스단추를 눌러서 화소를 설정하거나 지운다. 이때 단추를 누른 상태에서 화소를 끌고다니는 방법으로 화소를 설정하거나 지운다. 한번에 단추와 여러개의 건을 누를수 있으므로 QMouseEvent::state()가 돌려준 값은 마우스단추들(혹은 Shift와 Ctrl과 같은 수식건)의 비트별 OR이다. &연산자를 리용하여 어느 단추를 눌렀는가 검사하고 단추를 눌렀으면 setImagePixel()를 호출한다.

void IconEditor::setImagePixel(const QPoint &pos, bool opaque){

int i = pos.x() / zoom;

int j = pos.y() / zoom;

if (image.rect().contains(i, j)) {

if (opaque)

image.setPixel(i, j, penColor().rgb());

else

image.setPixel(i, j, qRgba(0, 0, 0, 0));

QPainter painter(this);

drawImagePixel(&painter, i, j);

}

}

setImagePixel()함수는 mousePressEvent()와 mouseMoveEvent()로부터 호출되고 화소를 설정하거나 지운다. pos파라메터는 창문부분품에서 마우스위치이다.

첫 단계는 마우스위치를 창문부분품자리표로부터 화상자리표로 변환하는것이다. 이것은 마우스위치의 x와 y요소들을 zoom곁수로 나누어 수행한다. 다음에 점이 정확히 범위안에 있는가 검사한다. 검사는 QImage::rect()와 QRect::contains()에 의해 쉽게 진행되는데 이때 i가 0과 image.width() – 1사이에, j는 0과 image.height() – 1사이에 있는가 검사한다.

opaque파라메터에 따라 화상의 화소를 설정하거나 지운다. 화소의 지우기는 실제로 화소를 투명으로 설정한다. 끝으로 drawImagePixel()를 호출하여 변경된 개별적인 화소를 다시 그린다.

구성자에서 사용한 WStaticContents기발은 Qt에 창문부분품의 크기가 달라질 때 창문부분품의 내용이 달라지지 않으며 그 내용은 창문부분품의 왼쪽웃구석에 고착된다는것을 의미한다. Qt는 이 정보를 리용하여 창문부분품크기가 달라질 때 이미 표시되여있는 구역을 필요없이 다시 그리는것을 피한다.

보통 창문부분품크기가 변경될 때 Qt는 창문부분품의 전체 보임구역에 대하여 그리기사건을 생성한다. 그러나 창문부분품을 WStaticContents기발을 리용하여 창조하면 그리기사건의 령역(region)은 이전에 표시되지 않은 화소들로 제한된다. 창문부분품의 크기가 더 작은 크기로 조절되면 그리기사건은 전혀 생성되지 않는다.

# 제2장. Qt응용프로그람의 사용자대면부관리

## 제1절. 구성배치관리

배치되는 매개 창문부분품에는 적당한 크기와 위치가 주어져야 한다. 일부 큰 창문부분품들은 사용자가 그 내용을 모두 호출하는데 흘림띠를 요구한다.

### 1. 기본배치

Qt는 자식창문부분품들의 배치를 관리하는 3가지 기본방법 즉 절대위치지정, 수동배치 및 배치관리자를 제공한다.

절대위치지정은 창문부분품들을 배치하는 가장 원시적인 방법이다. 절대위치지정은 자식창문부분품들에 고정크기와 위치를 할당하고 대면형식창에 고정크기를 할당하여 실현한다. FindFileDialog구성자에서 절대위치지정을 사용하는 방법에 대한 실례는 다음과 같다.

FindFileDialog::FindFileDialog(QWidget *parent, const char *name) : Qdialog (parent, name) {

...

namedLablel→setGeometry(10, 10, 50, 20);

namedLineEdit→setGeometry(70, 10, 200, 20);

lookInLabel→setGeometry(10, 35, 50, 20);

lookInLineEdit→setGeometry(70, 35, 200, 20);

subfoldersCheckBox→setGeometry(10, 60, 260, 20);

listView→setGeometry(10, 85, 260, 100);

messageLabel→setGeometry(10, 190, 260, 20);

findButton→setGeometry(275, 10, 80, 25);

stopButton→setGeometry(275, 40, 80, 25);

closeButton→setGeometry(275, 70, 80, 25);

helpButton→setGeometry(275, 185, 80, 25);

setFixedSize(365, 220);

}

절대위치지정에는 많은 결함이 있다. 첫째 문제는 사용자가 창문크기를 조절할수 없는것이다. 또 하나의 문제는 사용자가 큰 서체를 선택하거나 혹은 응용프로그람이 다른 언어로 번역되면 일부 본문이 잘리우는것이다. 그리고 이 수법은 또한 지루하게 위치와 크기를 계산하여야 한다.

절대위치를 지정하는 다른 수법은 수동배치이다. 수동배치(manual layout)에서는 창문부분품들이 여전히 절대위치로 주어지지만 그 크기는 완전히 고정되지 않고 창문크기에 비례하여 정해진다. 이것은 대면형식창의 resizeEvent()함수를 재정의하여 자식창문부분품의 기하학적형태를 설정하는 방법으로 달성한다.

FindFileDialog::FindFileDialog(QWidget *parent, const char *name) : QDialog(parent, name) {

...

setMinimumSize(215, 170); resize(365, 220);

}

void FindFileDialog::resizeEvent(QResizeEvent *){

int extraWidth = width() -minimumWidth();

int extraHeight = height() -minimumHeight();

namedLabel→setGeometry(10, 10, 50, 20);

namedLineEdit→setGeometry(70, 10, 50 + extraWidth, 20);

lookInLabel→setGeometry(10, 35, 50, 20);

lookInLineEdit→setGeometry(70, 35, 50 + extraWidth, 20);

subfoldersCheckBox→setGeometry(10, 60, 110 + extraWidth, 20);

listView→setGeometry(10, 85, 110 + extraWidth, 50 + extraHeight);

messageLabel→setGeometry(10, 140 + extraHeight, 110 + extraWidth, 20);

findButton→setGeometry(125 + extraWidth, 10, 80, 25);

stopButton→setGeometry(125 + extraWidth, 40, 80, 25);

closeButton→setGeometry(125 + extraWidth, 70, 80, 25);

helpButton→setGeometry(125 + extraWidth, 135 + extraHeight, 80, 25);

}

FindFileDialog구성자에서는 대면형식창의 최소크기를 215×170으로 설정하고 그 초기크기를 365×220으로 설정한다. resizeEvent()함수에서는 늘이려는 창문부분품들에 여유공간을 준다.

절대위치지정처럼 수동배치는 프로그람작성자가 계산해야 할 고정정수들을 많이 요구한다. 이러한 코드를 쓰면 설계가 달라지는 경우에 아주 시끄럽다. 그리고 여전히 본문이 잘리울 위험이 있다. 그러한 위험은 자식창문부분품들의 크기암시를 고려하여 피할수 있으나 그것은 코드를 더 복잡하게 만든다.

창문부분품들을 배치하는 가장 좋은 해결방안은 Qt의 배치관리자를 사용하는것이다. 배치관리자는 매개 형의 창문부분품에 의식할수 있는 기정값들을 제공하며 창문부분품의 서체, 형식, 내용에 의존하는 매개 창문부분품의 크기암시를 고려한다. 또한 배치관리자는 최소크기와 최대크기를 고려하고 서체변경, 본문변경, 창문크기변경에 대하여 자동적으로 배치를 조절한다.

Qt는 3가지 배치관리자 즉 QHBoxLayout, QVBoxLayout, QGridLayout를 제공한다. 이 클라스들은 QLayout를 계승한다. QLayout는 배치의 기본틀거리를 제공한다. 3개의 클라스들은 모두 Qt Designer에 의해 완전히 유지되여있고 코드에서도 사용할수 있다.

FindFileDialog::FindFileDialog(QWidget *parent, const char *name) : QDialog(parent, name) {

...

QGridLayout *leftLayout = new QGridLayout;

leftLayout→addWidget(namedLabel, 0, 0);

leftLayout→addWidget(namedLineEdit, 0, 1);

leftLayout→addWidget(lookInLabel, 1, 0);

leftLayout→addWidget(lookInLineEdit, 1, 1);

leftLayout→addMultiCellWidget(subfoldersCheckBox, 2, 2, 0, 1);

leftLayout→addMultiCellWidget(listView, 3, 3, 0, 1);

leftLayout→addMultiCellWidget(messageLabel, 4, 4, 0, 1);

QVBoxLayout *rightLayout = new QVBoxLayout;

rightLayout→addWidget(findButton);

rightLayout→addWidget(stopButton); rightLayout→addWidget(closeButton);

rightLayout→addStretch(1);

rightLayout→addWidget(helpButton);

QHBoxLayout *mainLayout = new QHBoxLayout(this);

mainLayout→setMargin(11);

mainLayout→setSpacing(6);

mainLayout→addLayout(leftLayout); mainLayout→addLayout(rightLayout);

}

배치는 QHBoxLayout, QGridLayout, QVBoxLayout에 의하여 조종된다.

QGridLayout는 왼쪽에, QVBoxLayout는 오른쪽에 나란히 배치되고 QHBoxLayout는 바깥쪽에 배치된다. 대화창주위의 여백은 11화소이고 자식창문부분품들사이의 공백은 6화소이다.

QGridLayout는 2차원살창의 세포들에 대하여 작업한다. 배치관리자의 왼쪽웃구석에 있는 QLabel은 위치 (0, 0)에, 대응하는 QLineEdit는 위치 (0, 1)에 있다. QCheckBox는 두 칸에 전개되여 위치 (2, 0)과 (2, 1)의 세포들을 차지한다. 그아래에 QListView와 QLabel도 두 칸에 전개된다. addMultiCellWidget()호출은 다음의 문법을 가진다.

leftLayout→addMultiCellWidget(widget, row1, row2, col1, col2);

여기서 widget는 배치관리자에 삽입하려는 자식창문부분품, (row1, col1)은 창문부분품이 차지한 왼쪽웃구석세포, (row2, col2)는 창문부분품이 차지한 오른쪽 아래구석세포이다.

Qt Designer에서 자식창문부분품들을 적당한 위치에 배치하고 배치할것들을 선택한 다음 Layout|Lay Out Horizontally, Layout|Lay Out Vertically, 혹은 Layout|Lay Out in a Grid를 찰칵하여 대화창을 시각적으로 창조할수 있다.

배치관리자에 창문부분품을 추가하거나 배치관리자에서 창문부분품을 삭제할 때 배치관리자는 자동적으로 새로운 경우에 적응된다. 또한 자식창문부분품에 대하여 hide()나 show()를 호출하여 적용할수도 있다. 자식창문부분품의 크기암시가 달라지면 배치관리자들은 자동적으로 새 크기암시를 고려하여 재시행된다. 또한 배치관리자들은 대면형식창의 자식창문부분품들의 최소크기와 크기암시들에 기초하여 대면형식창 전체의 최소크기를 자동적으로 설정한다.

배치하고있는 창문부분품들의 크기방략과 크기암시들을 변경하여 배치를 조절할수 있다.

창문부분품의 크기방략(size policy)은 배치체계에 창문부분품을 늘이거나 줄이는 방법을 말해준다. Qt는 자기의 모든 기본창문부분품들에 대하여 기정크기암시값들을 제공한다. 그러나 가능한 매개 배치관리자에 대하여 하나의 기정값만 고려할수 없으므로 대면형식창우의 하나이상의 창문부분품들에 대하여 크기방략들을 변경하는것은 개발자들에게 있어서 아직 관례로 되여있다. 크기암시는 수평 및 수직요소들을 모두 가진다. 매개 요소에 대한 가장 유효한 값들은 Fixed, Minimum, Maximum, Preferred, Expanding이다.

Preferred창문부분품과 Expanding창문부분품들을 모두 포함하는 대면형식창의 크기를 조절할 때 Expanding창문부분품들에 여유공간이 주어지고 Preferred창문부분품들은 자기 크기암시의 크기를 그대로 유지한다.

두가지 다른 크기방략 즉 MinimumExpanding과 Ignored가 있다.

MinimumExpanding은 Expanding을 사용하여 minimumSizeHint()을 적당히 재정의하는것이다. Ignored는 Expanding과 비슷한데 창문부분품의 크기암시를 무시한다는것이 다르다.

크기암시의 수평 및 수직요소들외에 QSizePolicy클라스는 수평 및 수직 늘임곁수(stretch factor)를 둘다 보유한다. 이 늘임곁수들은 대면형식창을 확장할 때 각이한 자식창문부분품들을 각이한 비률로 늘여야 한다는것을 지적하는데 쓰인다. 례를 들면 QTextEdit우에 QListView가 있고 QTextEdit를 QListView의 두배로 늘이려고 한다면 QTextEdit의 수직늘임곁수를 2로, QListView의 수직늘임곁수를 1로 설정한다.

배치에 영향을 주는 다른 수법은 자식창문부분품들에 대하여 최소크기, 최대크기 또는 고정크기를 설정하는것이다. 배치관리자는 창문부분품들을 배치할 때 이 제한들을 고려한다. 그리고 이것이 충분하지 않으면 늘 자식창문부분품의 클라스로부터 파생하고 sizeHint()를 재정의하여 필요한 크기암시를 얻는다.

### 2. 분할기

분할기(splitter)는 다른 창문부분품들을 포함하는 창문부분품으로서 창문부분품들을 분할기손잡이(handle)들에 의하여 분리한다. 사용자들은 손잡이를 끌기하여 분할기의 자식창문부분품들의 크기를 변경할수 있다. 흔히 분할기들은 사용자에게 조종권을 더 주기 위한 배치관리자들의 또 하나의 수법으로 사용된다.

Qt는 QSplitter창문부분품에 의해 분할기들을 유지한다. QSplitter의 자식창문부분품들은 그것이 창조되는 순서로 자동적으로 나란히(혹은 우아래로) 배치되고 이웃창문부분품들사이에는 분할띠(splitter bar)들이 있다.

#include <qapplication.h>

#include <qsplitter.h>

#include <Qtextedit.h>

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

QSplitter splitter(Qt::Horizontal);

splitter.setCaption(QObject::tr("Splitter"));

app.setMainWidget(&splitter);

QTextEdit *firstEditor = new QTextEdit(&splitter);

QTextEdit *secondEditor = new QTextEdit(&splitter);

QTextEdit *thirdEditor = new QTextEdit(&splitter);

splitter.show();

return app.exec();

}

실례는 QSplitter창문부분품에 의해 수평배치된 3개의 QTextEdit들로 이루어진다. 대면형식창의 자식창문부분품들을 배치만 하는 배치관리자와는 달리 QSplitter는 QWidget를 계승하고 다른 창문부분품처럼 사용할수 있다.

QSplitter는 자식창문부분품들을 수평 혹은 수직으로 배치한다. 복합배치는 수평 및 수직 QSplitter들을 겹쌓아서 얻을수 있다. QMainWindow파생클라스구성자의 코드실례는 오른변에 수직 QSplitter를 포함하는 수평 QSplitter로 이루어진다.

MailClient::MailClient(QWidget *parent, const char *name) : QMainWindow(parent, name) {

horizontalSplitter = new QSplitter(Horizontal, this);

setCentralWidget(horizontalSplitter);

foldersListView = new QListView(horizontalSplitter);

foldersListView→addColumn(tr("Folders"));

foldersListView→setResizeMode(QListView::AllColumns);

verticalSplitter = new QSplitter(Vertical, horizontalSplitter);

messagesListView = new QListView(verticalSplitter);

messagesListView→addColumn(tr("Subject"));

messagesListView→addColumn(tr("Sender"));

messagesListView→addColumn(tr("Date"));

messagesListView→setAllColumnsShowFocus(true);

messagesListView→setShowSortIndicator(true);

messagesListView→setResizeMode(QListView::AllColumns);

textEdit = new QTextEdit(verticalSplitter); textEdit→setReadOnly(true);

horizontalSplitter→setResizeMode(foldersListView, QSplitter::KeepSize);

verticalSplitter→setResizeMode(messagesListView, QSplitter::KeepSize);

...

readSettings();

}

우선 수평QSplitter를 창조하고 그것을 QMainWindow의 중심창문부분품으로 설정한다. 그다음 자식창문부분품들과 그것들의 자식창문부분품들을 창조한다.

사용자가 창문크기를 변경할 때 QSplitter는 보통 공간을 분배하여 관련된 자식창문부분품들의 크기가 같아지게 한다. Mail Client실례에서는 이러한 동작을 요구하지 않고 그대신 자식창문부분품들의 크기를 2개의 QListView가 관리할것을 요구하며 QTextEdit에 여유공간을 주려고 한다. 이것은 거의 마감에 2번의 setResizeMode()호출에 의해 달성된다.

응용프로그람이 기동할 때 QSplitter는 자식창문부분품들에게 그것들의 초기크기에 기초하여 적당한 크기를 준다. QSplitter::setSizes()를 호출하여 분할기손잡이를 프로그람적으로 이동할수 있다. 또한 QSplitter클라스는 자기의 상태를 보관하고 응용프로그람이 다음번에 실행될 때 상태를 되살리는 수단을 제공한다. 여기에 Mail Client의 설정을 보관하는 writeSettings()함수가 있다.

void MailClient::writeSettings() {

QSettings settings;

settings.setPath("software-inc.com", "MailClient");

settings.beginGroup("/MailClient");

QString str;

QTextOStream out1(&str);

out1 >> *horizontalSplitter;

settings.writeEntry("/horizontalSplitter", str);

QTextOStream out2(&str);

out2 >> *verticalSplitter;

settings.writeEntry("/verticalSplitter", str); settings.endGroup();

}

여기에 대응하는 readSettings()함수가 있다.

void MailClient::readSettings(){

QSettings settings;

settings.setPath("software-inc.com", "MailClient");

settings.beginGroup("/MailClient");

QString str1 = settings.readEntry("/horizontalSplitter");

QTextIStream in1(&str1);

in1 >> *horizontalSplitter;

QString str2 = settings.readEntry("/verticalSplitter");

QTextIStream in2(&str2);

in2 >> *verticalSplitter;

settings.endGroup();

}

이 함수들은 QTextIStream과 QTextOStream, 2개의 QTextStream편의파생클라스들에 기초하고있다.

기정으로 분할기손잡이는 사용자가 그것을 끌고다닐 때 선택창으로 표시되고 분할기손잡이의 어느 한쪽에 있는 창문부분품의 크기는 사용자가 마우스단추를 놓을 때만 조절된다. 실제로 QSplitter가 자식창문부분품들의 크기를 변경하기 위해서는 setOpaque Resize(true)를 호출하군한다.

QSplitter는 Qt Designer에 의하여 완전히 유지된다. 창문부분품들을 분할기에 넣기 위해서는 요구되는 위치에 자식창문부분품들을 대략적으로 배치하고 그것들을 선택한 다음 Layout|Lay Out Horizontally(in Splitter) 혹은 Layout|Lay Out Vertically(in Splitter)를 찰칵한다.

### 3. 흘림보기

QScrollView클라스는 흘림가능한 보기구역, 2개의 흘림띠, 하나의 《구석》창문부분품(보통 빈 QWidget)을 제공한다. 창문부분품에 흘림띠들을 추가하려면 자체로 QScrollBar들의 실례를 만들고 흘림기능을 실현하기보다 QScrollView를 사용하는것이 훨씬 더 간단하다.

QScrollView를 사용하는 가장 간단한 방법은 흘림띠를 추가하려는 창문부분품에 대하여 addChild()를 호출하는것이다. QScrollView는 자동적으로 창문부분품을 보기구역(QScrollView::viewport()를 통하여 호출할수 있다.)의 자식으로(이미 자식으로 설정되지 않는 경우에만) 설정한다.

#include <qapplication.h>

#include <qscrollview.h>

#include "iconeditor.h"

int main(int argc, char *argv[]){

QApplication app(argc, argv);

QScrollView scrollView;

scrollView.setCaption(QObject::tr("Icon Editor"));

app.setMainWidget(&scrollView);

IconEditor *iconEditor = new IconEditor;

scrollView.addChild(iconEditor); scrollView.show();

return app.exec();

}

기정으로 흘림띠들은 보기구역이 자식창문부분품보다 작을 때에만 표시된다. 다음과 같이 코드를 써서 흘림띠들이 늘 표시되게 할수 있다.

scrollView.setHScrollBarMode(QScrollView::AlwaysOn);

scrollView.setVScrollBarMode(QScrollView::AlwaysOn);

자식창문부분품의 크기암시가 달라질 때 QScrollView는 자동적으로 새로운 크기암시를 받아들인다.

창문부분품을 가지는 QScrollView를 사용하는 다른 방법은 창문부분품이 QScrollView를 계승하게 하고 내용을 그리는 drawContents()를 재정의하는것이다. 이것은 QIconView, QListBox, QListView, QTable, QTextEdit와 같은 Qt클라스들에서 사용한 수법이다. 일반적으로 창문부분품이 흘림띠들을 요구한다면 QScrollView의 파생클라스를 실현하는것이 좋은 생각이다.

그 작업방법을 보여주기 위하여 새로운 판의 IconEditor클라스를 QScrollView파생클라스로서 실현한다. 새 클라스를 ImageEditor라고 부르고 그 흘림띠들이 큰 화상을 조종할수 있게 만든다.

머리부화일은 원래 클라스와 거의 비슷하다. 주요한 차이는 QWidget대신에 QScrollView로부터 계승하는것이다. 클라스의 실현을 고찰할 때 다른 차이도 고찰한다.

ImageEditor::ImageEditor(QWidget *parent, const char *name)

: QScrollView(parent, name, WStaticContents | WNoAutoErase) {

curColor = black;

zoom = 8;

curImage.create(16, 16, 32); curImage.fill(qRgba(0, 0, 0, 0));

curImage.setAlphaBuffer(true);

resizeContents();

}

구성자는 WStaticContents와 WNoAutoErase기발들을 QScrollView에 넘긴다. 이 기발들은 실제로 보기구역에 설정된다. QScrollView의 기정값(Expanding, Expanding)이 적당하므로 크기암시를 설정하지 않는다.

원래 판에서는 Qt의 배치관리자들에 의하여 자체로 초기의 창문부분품크기를 선택할수 있으므로 구성자에서 updateGeometry()를 호출하지 않았다. 그러나 여기서는 QScrollView기초클라스에 작업하려는 초기크기를 주어야 하고 resizeContents()호출에서 이것을 수행한다.

void ImageEditor::resizeContents(){

QSize size = zoom * curImage.size();

if (zoom >= 3)

size += QSize(1, 1);

QScrollView::resizeContents(size.width(), size.height());

}

resizeContents()비공개함수는 QScrollView의 내용부분의 크기를 넘기여 QScroll View::resizeContents()를 호출한다. QScrollView는 보기구역이 내용부분의 어느 위치에 있는가에 따라 흘림띠들을 현시한다.

sizeHint()를 재정의할 필요는 없으며 QScrollView판은 내용의 크기를 리용하여 합리적인 크기암시를 제공한다.

void ImageEditor::setImage(const QImage &newImage) {

if (newImage != curImage) {

curImage = newImage.convertDepth(32);

curImage.detach();

resizeContents(); updateContents();

}

}

IconEditor의 많은 원시함수들에서는 update()를 호출하여 재그리기를 진행하고 updateGeometry()를 호출하여 크기암시변경을 전달하였다. QScrollView판에서는 이 함수호출들이 내용의 크기변경에 대하여 QScrollView에 통지하는 resizeContents()와 재그리기하게 하는 updateContents()로 교체된다.

void ImageEditor::drawContents(QPainter *painter, int, int, int, int) {

if (zoom >= 3) {

painter→setPen(colorGroup().foreground());

for (int i = 0; i <= curImage.width(); ++i)

painter→drawLine(zoom * i, 0, oom * i, zoom * curImage.height());

for (int j = 0; j <= curImage.height(); ++j)

painter→drawLine(0, zoom * j, zoom * curImage.width(), zoom * j);

}

for (int i = 0; i < curImage.width(); ++i) {

for (int j = 0; j < curImage.height(); ++j)

drawImagePixel(painter, i, j);

}

}

drawContents()함수는 QScrollView에 의해 호출되며 내용의 구역을 다시 그린다. QPainter객체는 이미 흘림변위를 계산하도록 초기화되여있다.

2～5번째 파라메터들은 다시 그려야 할 직4각형을 지정한다. 이 정보를 리용하여 다시 그려야 할 직4각형만 다시 그릴수 있지만 단순히 모두 다시 그린다.

drawContents()의 마감부근에서 호출되는 drawImagePixel()함수는 본질상 원래의 IconEditor클라스의 함수와 같으므로 여기서 다시 생성하지 않는다.

void ImageEditor::contentsMousePressEvent(QMouseEvent *event) {

if (event→button() == LeftButton)

setImagePixel(event→pos(), true);

else if (event→button() == RightButton)

setImagePixel(event→pos(), false);

}

void ImageEditor::contentsMouseMoveEvent(QMouseEvent *event) {

if (event→state() & LeftButton)

setImagePixel(event→pos(), true);

else if (event→state() & RightButton)

setImagePixel(event→pos(), false);

}

## 제2절. 사건처리

GUI응용프로그람들은 사건구동형이다. 즉 응용프로그람이 기동하면 발생하는것은 사건의 결과이다. Qt로 프로그람을 작성할 때 어떤 일이 발생하면 Qt창문부분품들이 신호들을 발생하므로 사건에 대하여 론의할 필요가 있다. 사건은 자체의 사용자정의창문부분품을 쓰거나 현존 Qt 창문부분품들의 동작을 수정하려고 할 때 사용할수 있다.

### 1. 사건처리함수의 재정의

사건은 여러가지 정황에 따라서 창문체계나 Qt에 의해 생성된다. 사용자가 건사건이나 마우스단추를 누르거나 놓으면 건이나 마우스사건이 생성된다. 창문이 이동하여 가리워졌던 다른 창문이 로출될 때 그리기사건이 생성되여 새로 보이는 창문에 다시 그리기하여야 한다는것을 알려준다. 또한 사건은 창문부분품이 건반초점을 얻거나 잃을 때마다 생성된다. 대부분의 사건은 사용자의 작용에 응답하여 생성되지만 시계사건 등 일부는 체계에 의해 독립적으로 생성된다.

사건을 신호와 혼돈하지 말아야 한다. 신호는 창문부분품을 리용할 때 필요하지만 사건은 창문부분품을 실현할 때 필요하다. 례를 들면 QPushButton을 사용하고있을 때 신호를 발생하는 저수준 마우스사건이나 건사건보다도 그 clicked()신호에 더 관심을 가진다. 그러나 QPushButton과 같은 클라스를 실현하고있으면 마우스와 건사건들을 조종하고 필요할 때 clicked()신호를 발생하는 코드를 써야 한다.

사건은 QObject로부터 계승된 event()함수를 통하여 객체들에 통지된다. QWidget에서 event()실현은 mousePressEvent(), keyPressEvent(), paintEvent()와 같은 특정한 사건처리함수들에 가장 보편적인 형태이고 다른 종류의 사건들은 무시한다.

사용자정의사건형들을 창조하고 사용자정의사건들을 자체로 발송할수 있다.

건사건들은 keyPressEvent()와 keyReleaseEvent()를 재정의하여 처리한다. Plotter창문부분품은 keyPressEvent()를 재정의한다. 보통 놓기에서 중요한 건이란 수식건 Ctrl, Shift, Alt이고 이 건들은 state()를 사용하여 keyPressEvent()에서 검사할수 있으므로 keyPressEvent()를 재정의할 필요가 있다. 례를 들면 CodeEditor창문부분품을 실현하는 경우에 Home과 Ctrl+Home사이를 구별하는 keyPressEvent()는 다음과 같을수 있다.

void CodeEditor::keyPressEvent(QKeyEvent *event) {

switch (event→key()) {

case Key_Home:

if (event→state() & ControlButton)

goToBeginningOfDocument();

else goToBeginningOfLine();

break;

case Key_End: ...

default:

QWidget::keyPressEvent(event);

}

}

Tab와 Backtab(Shift+Tab)건들은 특수한 경우이다. 이것들은 초점사슬에서 다음 또는 이전의 창문부분품으로 초점을 넘긴다는 의미에서 keyPressEvent()를 호출하기 전에 QWidget::event()에 의해 처리된다. 이 동작은 보통 경우에는 맞지만 CodeEditor창문부분품에서는 Tab를 사용하여 행의 들여쓰기를 진행한다. 그때 event()재정의는 다음과 같다.

bool CodeEditor::event(QEvent * event) {

if (event→type() == QEvent::KeyPress) {

QKeyEvent *keyEvent = (QKeyEvent *)event;

if (keyEvent→key() == Key_Tab) {

insertAtCurrentPosition('\t');

return true;

}

}

return QWidget::event(event);

}

사건이 건누르기이면 QEvent객체를 QKeyEvent로 강제변환하고 어느 건이 눌러졌는가를 검사한다. 건이 Tab이면 그에 대한 처리를 수행하고 true를 돌려주어 Qt에게 사건을 처리했다고 알린다. false를 돌려주었으면 Qt는 사건을 부모창문부분품에 전달한다.

건속박을 실현하는 고급한 수법은 QAction을 사용하는것이다. 례를 들면 goToBeginningOfLine()과 goToBeginningOfDocument()가 CodeEditor창문부분품에서 공개처리부들이고 CodeEditor가 MainWindow클라스의 중심창문부분품으로 사용된다면 다음의 코드로 건결합을 추가할수 있다.

MainWindow::MainWindow(QWidget *parent, const char *name):

QMainWindow(parent, name){

editor = new CodeEditor(this);

setCentralWidget(editor);

goToBeginningOfLineAct = new QAction(tr("Go to Beginning of Line"), tr("Home"), this);

connect(goToBeginningOfLineAct, SIGNAL(activated()), editor,

SLOT(goToBeginningOfLine()));

goToBeginningOfDocumentAct=new QAction(tr("Go to Beginning of Document"),

tr("Ctrl+Home"), this);

connect(goToBeginningOfDocumentAct, SIGNAL(activated()), editor, SLOT (goToBeginningOfDocument()));

...

}

이것은 차림표나 도구띠에 지령들을 간단히 추가하게 한다. 지령이 사용자대면부에 나타나지 않으면 QAction객체들은 건결합을 유지하기 위하여 내적으로 QAction에 의해 사용되는 클라스인 QAccel객체로 교체된다.

keyPressEvent()재정의와 QAction(혹은 QAccel)사용사이의 선택은 resizeEvent()재정의와 QLayout파생클라스사용사이의 선택과 비슷하다. QWidget의 파생클라스를 만들어 사용자정의창문부분품을 실현한다면 일부 사건처리함수들을 재정의하고 거기에 동작코드를 간단히 쓸수 있다. 그러나 단지 창문부분품을 사용한다면 QAction과 QLayout에 의해 제공되는 고수준대면부들이 더 편리하다.

또 하나의 일반사건은 시계사건이다. 대부분의 사건은 사용자작용의 결과로 발생하지만 시계사건은 응용프로그람이 규칙적인 시격으로 처리를 수행하게 한다. 시계사건은 마우스지시자의 깜빡거림이 없는 동화를 실현하거나 현시기를 초기화하는데 쓰일수 있다.

시계사건을 보여주기 위하여 Ticker창문부분품을 실현한다. 이 창문부분품은 30㎳마다 1화소씩 왼쪽으로 흘러가는 본문띠(banner)를 표시한다. 창문부분품의 폭이 본문보다 더 넓으면 본문은 창문부분품의 전체폭을 채우도록 필요한만큼 반복된다.

hideEvent()함수는 QObject::killTimer()를 호출하여 시계를 중지한다.

시계사건들은 저수준이고 여러개의 시계가 요구되면 시계ID들을 추적하여 보관하는것이 불편하다. 그러한 경우에 보통 매개 시계에 대하여 QTimer객체를 창조하는것이 더 편리하다. QTimer는 매 시간간격마다 timeout()신호를 발생한다. 또한 QTimer는 단일발사시계(한번만 시간을 요구하는 시계)에 편리한 대면부를 제공한다.

### 2. 사건려과기의 설치

Qt사건모형의 한가지 강력한 특성은 어떤 QObject실례가 자기 사건들을 알아보기전에 다른 QObject실례가 그 사건들을 감시하도록 설정할수 있는것이다.

여러개의 QLineEdit들로 구성된 CustomerInfoDialog창문부분품이 있고 Space건으로 초점을 다음 QLineEdit로 옮기려고 한다고 하자. 이것은 QLineEdit의 파생클라스를 만들고 keyPressEvent()를 재정의하여 focusNextPrevChild()를 호출함으로써 실현할수 있다.

void MyLineEdit::keyPressEvent(QKeyEvent *event) {

if (event→key() == Key_Space)

focusNextPrevChild(true);

else

QLineEdit::keyPressEvent(event);

}

이 수법에는 많은 결함이 있다. MyLineEdit가 표준Qt클라스가 아니므로 그것을 사용하는 대면형식창을 설계하려면 Qt Designer에 통합되여야 한다. 또한 대면형식창에서 각종 창문부분품(례를 들면 QComboBox와 QSpinBox)들을 여러개 사용한다면 그것들을 파생클라스로 만들어 같은 동작을 보여주게 하고 Qt Designer에 통합하여야 한다.

더 좋은 해결책은 CustomerInfoDialog가 자식창문부분품들의 건누르기사건들을 감시하게 하고 감시코드에 필요한 동작을 실현하는것이다. 이것은 사건려과기에 의해 달성된다. 사건려과기는 2단계에 걸쳐 설치한다.

① 목표에 대하여 installEventFilter()를 호출하여 목표객체와 함께 감시객체를 등록한다.

② 감시기의 eventFilter()함수에서 목표객체의 사건들을 처리한다.

감시객체를 등록하는 좋은 위치는 CustomerInfoDialog구성자이다.

CustomerInfoDialog::CustomerInfoDialog(QWidget *parent, const char *name): QDialog(parent, name){

...

firstNameEdit→installEventFilter(this); lastNameEdit→installEventFilter(this);

cityEdit→installEventFilter(this); phoneNumberEdit→installEventFilter(this);

}

사건려과기가 등록되면 firstNameEdit, lastNameEdit, cityEdit, phoneNumberEdit창문부분품들에 송신되는 사건들은 자기의 예정된 목적지에 송신되기 전에 Customer InfoDialog의 eventFilter()함수에 우선 송신된다.(여러개의 사건려과기가 같은 객체에 설치되여있으면 려과기들은 제일 최근에 설치된것부터 차례로 능동화된다.)

여기에 사건들을 받아들이는 eventFilter()함수가 있다.

bool CustomerInfoDialog::eventFilter(QObject *target, QEvent *event) {

if (target == firstNameEdit || target == lastNameEdit

|| target == cityEdit || target == phoneNumberEdit) {

if (event→type() == QEvent::KeyPress) {

QKeyEvent *keyEvent = (QKeyEvent *) event;

if (keyEvent→key() == Key_Space) {

focusNextPrevChild(true);

return true;

}

}

}

return QDialog::evenFilter(target, event);

}

우선 목표창문부분품이 QLineEdit들중 하나인가 검사한다. 기초클라스 QDialog는 자기의 창문부분품들을 감시할수 있다.

사건이 건누르기이면 그것을 QKeyEvent로 강제변환하고 어느건을 눌렀는가 검사한다. 누른 건이 Space이면 focusNextPrevChild()를 호출하여 초점을 초점사슬의 다음 창문부분품에 넘기고 true를 돌려주어 Qt에게 사건을 처리하였다는것을 알린다. false를 돌려주면 Qt는 사건을 예정한 목표에 보내고 결과 공백의 가상코드가 QLineEdit에 삽입된다.

사건이 Space건누르기가 아니면 조종을 eventFilter()의 기초클라스실현에 넘긴다.

Qt는 사건들을 처리하고 려과하는 5개의 준위를 제공한다.

① 특정한 사건처리함수를 재정의할수 있다.

mousePressEvent(), keyPressEvent(), paintEvent()와 같은 사건처리함수들의 재정의는 사건들을 처리하는 가장 일반적인 방법이다.

② QObject::event()를 재정의할수 있다.

event()함수를 재정의함으로써 사건이 특정한 사건처리함수들에 도달하기 전에 처리된다.

이 수법은 처음에 보여준것처럼 Tab건의 기정의미를 무시하는데 대체로 필요하다. 이것은 또한 특정한 사건처리함수가 존재하지 않는 사건(례를 들면 LayoutDirectionChange)들처럼 드물게 나타나는 사건들을 처리하는데 쓰인다. event()를 재정의할 때 정확히 처리하지 못하는 경우를 취급하기 위하여 기초클라스의 event()함수를 호출해야 한다.

③ 하나의 QObject에 사건려과기를 설치할수 있다.

installEventFilter()에 의해 객체를 등록하였다면 목표객체의 모든 사건들은 우선 감시객체의 eventFilter()함수에 송신된다. 이 수법을 리용하여 우의 CustomerInfoDialog실례에서 Space건누르기를 처리하였다.

④ QApplication객체에 사건려과기를 설치할수 있다.

사건려과기가 qApp(유일한 QApplication객체)용으로 등록되였다면 응용프로그람안의 매개 객체에 대한 매개 사건은 다른 사건려과기에 송신되기 전에 eventFilter()함수에 송신된다. 이 수법은 오유수정에 사용할수 있다. 또한 QApplication이 보통 무시하는 금지된 창문부분품들에 송신된 마우스사건들을 처리하는데 쓰일수도 있다.

⑤ QApplication의 파생클라스를 만들고 notify()를 재정의할수 있다.

Qt는 QApplication::notify()를 호출하여 사건을 송신한다. 이 함수의 재정의는 사건려과기의 사건들을 볼 기회를 얻기 전에 모든 사건들을 얻는 유일한 방법이다. 일반적으로 여러개의 사건려과기들이 동시에 있을수 있으나 notify()함수는 오직 하나이므로 사건려과기는 더 효과있다.

마우스와 건사건들을 비롯한 많은 사건형들을 전달할수 있다. 사건이 그 목표객체에로 가는 도중에 혹은 목표객체자체에 의하여 처리되지 않았다면 전체사건처리과정은 목표객체의 부모를 새 목표로 하여 반복된다. 이 과정은 사건이 처리되거나 제일 웃준위객체에 이를 때까지 부모들을 따라 올라가면서 계속된다.

### 3. 응답성지연

QApplication::exec()를 호출할 때 Qt의 사건순환고리를 기동한다. Qt는 기동시에 몇가지 사건들을 발생하여 창문부분품들을 표시하고 그린다. 그후에 사건순환고리를 실행하고 늘 사건이 발생하였는가 확인하고 사건들을 응용프로그람의 QObject들에 발송한다.

하나의 사건을 처리하는 도중에 다른 사건들이 생성되여 Qt의 사건대기렬에 추가될수 있다. 그러면 특정한 사건의 처리에 너무 많은 시간을 소비하고 사용자대면부의 반응이 떠진다. 례를 들면 응용프로그람이 화일을 디스크에 보관하는 동안에 창문체계에 의하여 생성된 사건들은 화일이 보관될 때까지 처리되지 않는다. 보관하는 동안 응용프로그람은 창문체계로부터 자체를 다시 그리려는 요구에 응답하지 않는다.

하나의 해결책은 여러개의 스레드를 사용하는것이다. 즉 하나는 응용프로그람의 사용자대면부용스레드이고 다른 하나는 화일보관(혹은 시간을 소비하는 다른 조작)을 수행하는 스레드이다. 이렇게 응용프로그람의 사용자대면부는 화일을 보관하는 동안 계속 응답성을 유지한다.

화일보관코드에서 QApplication::processEvents()를 자주 호출하는것이다.

이 함수는 Qt가 대기하고있는 사건들을 처리하고 조종을 호출자에게 돌려준다. 사실상 QApplication::exec()는 while순환보다 processEvents()함수호출부근에 더 많다.

여기에 processEvents()를 리용하여 사용자대면부가 응답성을 지연하는 실례가 있다.

이 실례는 Spreadsheet의 화일보관코드에 기초하고있다.

bool Spreadsheet::writeFile(const QString &fileName){

QFile file(fileName);

...

for (int row = 0; row < NumRows; ++row) {

for (int col = 0; col < NumCols; ++col) {

QString str = formula(row, col);

if (!str.isEmpty())

out << (Q_UINT16)row << (Q_UINT16)col << str;

}

qApp→processEvents();

}

return true;

}

이 수법에서 한가지 위험한것은 현재 응용프로그람이 보관중에 있는데 사용자가 기본창문을 닫거나 지어는 File|Save를 찰칵하여 정의되지 않은 동작이 발생하는것이다. 이 문제를 해결하는 가장 간단한 방법은 다음의 호출 qApp→processEvents();를 Qt에게 마우스와 건사건들을 무시하게 하는 다음의 호출로 바꾸는것이다.

qApp→eventLoop()→processEvents(QEventLoop::ExcludeUserInput);

흔히 오래동안 실행하는 조작이 발생하였을 때 QProgressDialog를 표시하려고 한다.

QProgressDialog는 응용프로그람에 의해 이루어지는 진행정형에 대하여 사용자에게 통지하는 진행띠를 가지고있다. 또한 QProgressDialog는 사용자가 조작을 중지하게 하는 Cancel단추를 제공한다. 여기에 이 수법으로 Spreadsheet화일을 보관하는 코드가 있다.

bool Spreadsheet::writeFile(const QString &fileName){

QFile file(fileName);

...

QProgressDialog progress(tr("Saving file..."), tr("Cancel"), NumRows);

progress.setModal(true);

for (int row = 0;row < NumRows;++row) {

progress.setProgress(row);

qApp→processEvents();

if (progress.wasCanceled()) {

file.remove();

return false;

}

for (int col = 0;col < NumCols;++col) {

QString str = formula(row, col);

if (!str.isEmpty())

out << (Q_UINT16)row << (Q_UINT16)col << str;

}

}

return true;

}

총걸음수가 NumRows인 QProgressDialog를 창조한다. 그다음 각 행에 대하여 setProgress()를 호출하여 진척상태띠를 갱신한다. QProgressDialog는 자동적으로 현재 진행정형값을 총걸음수로 나누어 퍼센트를 계산한다. QApplication::processEvents()를 호출하여 재그리기사건이나 사용자의 찰칵 혹은 건누르기로 처리한다.(례를 들면 사용자가 Cancel을 찰칵하게 한다.) 사용자가 Cancel을 찰칵하면 보관을 중지하고 화일을 삭제한다.

QProgressDialog에 대해서는 show()를 호출하지 않는다. 그것은 진척상태대화칸이 그 일을 자체로 수행하기때문이다. 보관하려는 화일이 작거나 콤퓨터가 고속이여서 조작이 짧은 시간에 끝난다면 QProgressDialog는 이것을 탐지하고 그 자체를 전혀 표시하지 않는다.

실행시간이 긴 조작을 처리하는 완전히 다른 수법이 있다. 사용자가 요구할 때 처리를 수행하지 않고 응용프로그람이 무부하로 될 때까지 처리를 연기하는것이다. 이것은 응용프로그람이 얼마나 오래동안 무부하상태인가를 예견할수 없으므로 처리를 안전하게 중단하였다가 되살릴수 있다면 작업이 가능하다.

Qt에서 이 수법은 특수한 종류의 시계 즉 0㎳시계를 리용하여 실현할수 있다. 이 시계들은 대기하고있는 사건이 없을 때 시간을 요구한다. 여기에 그 처리수법을 보여주는 timerEvent()실현의 실례가 있다.

void Spreadsheet::timerEvent(QTimerEvent*event) {

if (event→timerId() == myTimerId) {

while (step < MaxStep && !qApp→hasPendingEvents()) {

performStep(step);

++step;

}

} else

QTable::timerEvent(event);

}

hasPendingEvents()가 true를 돌려주면 처리를 중지하고 조종을 Qt에 돌려준다. 처리는 Qt가 대기하고있는 사건들을 모두 처리했을 때 되살아난다.

## 제3절. 도형처리

Qt의 2차원그리기는 QPainter로서 화면우의 창문부분품, 화면밖의 화소배렬 혹은 인쇄기에 그리는데 사용될수 있다. 또한 Qt는 도형처리를 수행하는 고급한 방법을 제공하는 QCanvas클라스를 포함한다. 여기서는 여러가지 형태의 수천개 항목들을 효과적으로 처리할수 있는 항목에 기초한 수법을 리용한다.

QPainter와 QCanvas외에 또한 OpenGL서고를 사용하는 방법이 있다. OpenGL은 3차원도형을 그리기 위한 표준서고이지만 2차원도형그리기에도 사용할수 있다.

### 1. QPainter에 의한 그리기

QPainter는 창문부분품이나 화소배렬과 같은 《그리기장치》에 그리기할 때 사용할수 있다. QPainter는 자체의 형식을 가지는 사용자정의창문부분품들이나 사용자정의항목클라스들을 쓸 때 효과있다.

QPainter는 QWidget, QImage, QPixmap, QGLWidget, QGLPixelBuffer, QPicture, QPrinter 등과 같은 QPaintDevice의 자식클라스우에서 그리기를 진행한다.

QPainter는 기하학적도형들인 점, 선, 직4각형, 타원, 호, 현, 부채형, 다각형, 3차베제곡선을 그릴수 있다. 또한 화소배렬, 화상, 본문도 그릴수 있다.

QPainter구성자에 그리기장치를 넘길 때 QPainter는 장치로부터 일부 환경설정을 받아들이고 다른 환경설정을 기정값으로 설정한다. 이 설정은 그리기를 수행하는 방법에 영향을 준다. 3가지 가장 중요한것은 그리기장치의 펜, 붓, 서체이다.

·펜은 직선과 기하학적도형의 테두리를 그리는데 사용된다. 펜은 색갈, 두께, 선형식, 모자(cap)형식, 결합형식으로 이루어진다.

·붓은 기하학적도형을 채우는데 사용되는 패턴이다. 붓은 색갈과 형식으로 이루어진다.

·서체는 본문을 그리는데 쓰인다. 서체는 계렬과 점크기 등 많은 속성들을 가지고있다. 이러한 설정은 QPen, QBrush 혹은 QFont객체에서 setPen(), setBrush(), setFont()를 호출하여 변경할수 있다.

타원을 그리는 코드는 다음과 같다.

QPainter painter(this);

painter.setPen(QPen(black, 3, DashDotLine));

painter.setBrush(QBrush(red, SolidPattern));

painter.drawEllipse(20, 20, 100, 60);

부채형을 그리는 코드는 다음과 같다.

QPainter painter(this);

painter.setPen(QPen(black, 5, SolidLine));

painter.setBrush(QBrush(red, DiagCrossPattern));

painter.drawPie(20, 100, 60, 60 * 16, 270 * 16);

drawPie()의 마지막 2개 인수는 시작각도와 마감각도를 16배한것이다.

3차원베제곡선을 그리는 코드는 다음과 같다.

QPainter painter(this);

QPointArray points(4);

points[0] = QPoint(20, 80); points[1] = QPoint(50, 20);

points[2] = QPoint(80, 20); points[3] = QPoint(120, 80);

painter.setPen(QPen(black, 3, SolidLine));

painter.drawCubicBezier(points);

그리기장치의 현재 상태는 save()호출에 의해 탄창에 보관되고 후에 restore()를 호출할 때 되살아난다. 이것은 그리기장치의 설정을 일시 변경하였다가 이전값들로 재설정하려고 할 때 쓸모있다.

펜, 붓, 서체외에 그리기장치를 조종하는 다른 설정은 다음과 같다.

·배경색은 배경방식이 OpaqueMode(기정값은 TransparentMode)일 때 기하도형, 본문 혹은 비트매프의 배경을 붓패턴으로 채우는데 리용한다.

·라스터조작(raster operation)은 그리기장치에 이미 표시되여있는 화소들과 새로 그려지는 화소들을 결합하는 방법을 지정한다. 기정값은 CopyROP로서 새 화소가 이전 화소값을 무시하고 장치에 단순히 복사된다는것을 의미한다. 다른 라스터조작으로서 XorROP, NotROP, AndROP, NotAndROP가 있다.

·붓원점은 붓패턴의 시작점으로서 보통 창문부분품의 왼쪽웃구석이다.

·잘라내기령역(clip region)은 그리기할수 있는 장치의 구역이다. 잘라내기령역밖에서 수행한 그리기조작은 무시된다.

·보기구역, 창문, 공간행렬(world matrix)은 론리 QPainter자리표를 물리적인 그리기장치자리표로 넘기는 방법을 결정한다. 기정으로 론리와 물리적인 자리표계들은 일치하도록 설정된다.

보기구역, 창문, 세계행렬에 의하여 정의된 자리표계를 더 구체적으로 고찰하자.(이 경우에 《창문》이라는 용어는 제일 웃준위 창문부분품의 의미에서 창문을 말하는것이 아니며 또 《보기구역》은 QScrollView의 보기구역에서 수행해야 하는 일을 가지고있는것이 아니다.) 보기구역과 창문은 정확히 한계가 있다. 보기구역(viewport)은 물리적인 자리표로 지정된 임의의 직4각형이다. 창문(window)은 같은 직4각형을 지정하지만 론리자리표로 되여있다. 그리기할 때에는 점들을 론리자리표로 지정하고 이 자리표들은 현재의 창문–보기구역설정에 기초하는 선형대수적방법에 의하여 물리적인 자리표로 변환된다. 기정으로 보기구역과 창문은 장치의 직4각형으로 설정된다. 례를 들면 장치가 320×200인 창문부분품이면 보기구역과 창문은 꼭같이 왼쪽웃구석의 위치가 (0, 0)인 320×200인 직4각형이다. 이 경우에 론리자리표계와 물리적인 자리표계는 같다. 창문–보기구역기구는 그리기장치의 크기나 분해능에 의존하지 않는 그리기코드를 작성하는데 쓸모있다. 항상 산수적으로 론리자리표를 물리자리표로 넘길수 있지만 QPainter가 그리도록 하는것이 좋다. 례를 들면 중심이 (0, 0)인 론리자리표를 (-50, -50)으로부터 (+50, +50)까지 전개하려고 한다면 창문을 다음과 같이 설정할수 있다.

painter.setWindow(QRect(-50, -50, 100, 100));

(-50, -50)쌍은 원점을 지정하고 (100, 100)쌍은 폭과 높이를 지정한다. 이것은 론리자리표 (-50, -50)이 현재 물리적인 자리표 (0, 0)에 대응되고 론리자리표 (+50, +50)이 물리적인 자리표 (320, 200)에 대응된다는것을 의미한다. 이 실례에서 보기구역을 변경할 필요는 없다.

그림 2‐1. 론리자리표를 물리적인 자리표로 변환

공간행렬은 창문–보기구역변환과 함께 적용되는 변환행렬이다. 이것은 그리고있는 항목들을 변환하고 신축하고 회전하거나 자르게 한다. 례를 들면 본문을 45°각으로 그리려고 한다면 다음의 코드를 사용할수 있다.

QWMatrix matrix;

matrix.rotate(45.0);

painter.setWorldMatrix(matrix);

painter.drawText(rect, AlignCenter, tr("Revenue"));

drawText()에 넘기는 론리자리표들은 공간행렬로 변환된 다음 창문–보기구역설정을 리용하여 물리적인 자리표로 넘어간다. 다중변환을 지정하면 변환들이 주어지는 차례로 적용된다. 례를 들면 회전축점으로서 점 (10, 20)을 리용하려고 한다면 창문을 변환하고 회전한 다음 창문을 원래 위치로 다시 변환한다.

QWMatrix matrix;

matrix.translate(-10.0, -20.0); matrix.rotate(45.0);

matrix.translate(+10.0, +20.0);

painter.setWorldMatrix(matrix); painter.drawText(rect, AlignCenter, tr("Revenue"));

변환을 지정하는 더 간단한 방법은 QPainter의 translate(), scale(), rotate(), shear()편의함수들을 사용하는것이다.

painter.translate(-10.0, -20.0); painter.rotate(45.0);

painter.translate(+10.0, +20.0);

painter.drawText(rect, AlignCenter, tr("Revenue"));

그러나 같은 변환을 반복하려고 한다면 변환들을 QWMatrix객체에 보관하고 변환이 필요할 때마다 그리기장치에 세계행렬을 설정하는것이 더 빠르다.

공간행렬을 보관하였다가 후에 되살리려면 saveWorldMatrix()와 restoreWorld Matrix()를 리용할수 있다.

OvenTimer창문부분품은 내부에 시계를 가지고있는 로에서 일반적으로 사용하고있는 물리적인 로(oven)시계를 모형화한것이다. 사용자는 눈금(notch)을 찰칵하여 지속시간을 설정할수 있다. 바퀴는 자동적으로 0에 이를 때까지 시계바늘과 반대방향으로 돌아가며 0점에서 OvenTimer는 timeout()신호를 발생한다. OvenTimer클라스는 QWidget를 계승하며 2개의 가상함수 paintEvent()와 mousePressEvent()를 재정의한다.

#include <qpainter.h>

#include <qpixmap.h>

#include <Qtimer.h>

#include <cmath>

#include "oventimer.h"

using namespace std;

const double DegreesPerMinute = 7.0;

const double DegreesPerSecond = DegreesPerMinute / 60;

const int MaxMinutes = 45;

const int MaxSeconds = MaxMinutes * 60;

const int UpdateInterval = 10;

OvenTimer::OvenTimer(QWidget *parent, const char *name) : QWidget(parent, name)

{

finishTime = QDateTime::currentDateTime();

updateTimer = new QTimer(this); finishTimer = new QTimer(this);

connect(updateTimer, SIGNAL(timeout()), this, SLOT(update()));

connect(finishTimer, SIGNAL(timeout()), this, SIGNAL(timeout()));

}

구성자에서는 2개의 QTimer객체를 창조하는데 updateTimer는 창문부분품의 모양을 규칙적인 시간간격으로 갱신하는데 쓰이고 finishTimer는 시계가 0에 이를 때 창문부분품의 timeout()신호를 발생한다.

void OvenTimer::setDuration(int secs) {

if (secs > MaxSeconds)

secs=MaxSeconds;finishTime= DateTime::currentDateTime().addSecs(secs);

updateTimer→start(UpdateInterval * 1000, false);

finishTimer→start(secs * 1000, true);

update();

}

setDuration()함수는 로시계의 지속시간을 주어진 초수로 설정한다. updateTimer의 start()호출에 넘기는 false인수는 Qt에 이것이 10s간격으로 시간을 요구하는 반복시계라는것을 말해준다.

finishTimer는 한번 시간을 요구하는데 필요하므로 true인수를 리용하여 그것이 단일발사시계라는것을 가리킨다. 초단위의 지속시간을 QDateTime::currentDateTime()에 의해 얻어진 현재 시간에 더하여 완료시간을 계산하고 finishTime비공개변수에 보관한다.

finishTime변수는 날자와 시간을 보관하는 Qt자료형인 QDateTime형이다. QDateTime의 date요소는 현재 시간이 자정전이고 완료시간이 자정후인 경우에 중요하다.

int OvenTimer::duration() const {

int secs = QDateTime::currentDateTime().secsTo(finishTime);

if (secs < 0)

secs = 0;

return secs;

}

duration()함수는 시계가 완료하기 전에 남은 초수를 돌려준다.

void OvenTimer::mousePressEvent(QMouseEvent *event) {

QPoint point = event→pos() -rect().center();

double theta = atan2(-(double)point.x(), -(double)point.y())*180 / 3.14159265359;

setDuration((int)(duration() + theta / DegreesPerSecond));

update();

}

사용자가 창문부분품을 찰칵하면 효과적인 수학식을 리용하여 가장 가까운 눈금을 찾아내고 결과를 리용하여 새 지속시간을 설정한다. 그다음 재그리기를 발생한다. 사용자가 찰칵한 눈금은 현재 제일 우에 있으며 0에 이를 때까지 시계바늘방향으로 이동한다.

void OvenTimer::paintEvent(QPaintEvent *) {

QPainter painter(this);

int side = QMIN(width(), height());

painter.setViewport((width() -side)/2, (height() -side)/2, side, side);

painter.setWindow(-50, -50, 100, 100);

draw(&painter);

}

paintEvent()에서는 보기구역을 창문부분품에 알맞는 최대 바른4각형구역으로 설정하고 창문을 직4각형(-50, -50, 100, 100) 즉 (-50, -50)으로부터 (+50, +50)범위의 100×100인 직4각형으로 설정한다. QMIN()마크로는 2개 인수의 최소값을 돌려준다.

보기구역을 바른4각형으로 설정하지 않았으면 로시계는 창문부분품이 바른4각형이 아닌 직4각형으로 크기가 달라질 때 타원으로 된다. 일반적으로 그러한 변형을 피하려면 보기구역과 창문을 같은 가로세로비를 가지는 직4각형들로 설정해야 한다.

또한 (-50, -50, 100, 100)의 창문은 아래와 같은 원인을 고려하여 설정되였다.

·QPainter의 draw함수들은 int자리표값들을 가진다. 창문을 너무 작게 선택하면 필요한 모든 점을 옹근수로 지정할수 없다.

·큰 창문을 사용하고 drawText()을 리용하여 본문을 그리려면 그것을 보상하는데 더 큰 서체가 요구된다.

이것은 말하자면 (-5, -5, 10, 10) 혹은 (-2 000, -2 000, 4 000, 4 000)보다 (-50, -50, 100, 100)이 더 좋은 선택으로 되게 한다.

void OvenTimer::draw(QPainter *painter) {

static const QCOORD triangle[3][2] ={{-2, -49}, {+2, -49}, {0, -47}};

QPen thickPen(colorGroup().foreground(), 2);

QPen thinPen(colorGroup().foreground(), 1);

painter→setPen(thinPen);

painter→setBrush(colorGroup().foreground());

painter→drawConvexPolygon(QPointArray(3, &triangle[0] [0]));

painter→setPen(thickPen);

painter→setBrush(colorGroup().light());

painter→drawEllipse(-46, -46, 92, 92);

painter→setBrush(colorGroup().mid());

painter→drawEllipse(-20, -20, 40, 40); painter→drawEllipse(-15, -15, 30, 30);

int secs = duration();

painter→rotate(secs*DegreesPerSecond);

painter→drawRect(-8, -25, 16, 50);

for (int i = 0;i <= MaxMinutes;++i) {

if (i % 5 == 0) {

painter→setPen(thickPen);

painter→drawLine(0, -41, 0, -44);

painter→drawText(-15, -41, 30, 25, AlignHCenter | AlignTop, QString::number(i));

} else {

painter→setPen(thinPen);

painter→drawLine(0, -42, 0, -44);

}

painter→rotate(-DegreesPerMinute);

}

}

창문부분품의 꼭대기에 0위치를 표식하는 아주 작은 3각형을 그리는것으로 시작한다. 3각형을 3개의 고정자리표들로 지정하고 drawConvexPolygon()을 리용하여 그린다. drawPolygon()을 리용할수 있으나 그리고 있는 다각형이 불록하다는것을 알고있을 때 drawConvexPolygon()을 호출하여 조금이나마 시간을 절약할수 있다.

창문–보기구역기구가 아주 편리한것은 그리기지령들에서 사용하는 자리표들을 고정코드화하여도 좋은 크기조절동작을 얻을수 있는것이다. 바른4각형이 아닌 창문부분품들에 대하여 걱정하지 않아도 보기구역을 적당히 설정하여 처리한다.

바깥원과 2개의 아낙원을 그린다. 바깥원은 조색판의 《밝은》요소(일반적으로 백색)로 채우고 아낙원들은 《중간》요소(일반적으로 중간재색)로 채운다.

손잡이, 눈금 그리고 5번째의 매개 눈금마다 분을 그린다. rotate()를 호출하여 그리기장치의 자리표계를 회전한다. 낡은 자리표계에서 0min표식은 제일 우에 있고 현재 0min표식은 나머지 시간에 적합한 위치로 이동된다. 직4각형손잡이의 방향이 회전각도에 의존하므로 회전후에 손잡이를 그린다.

for순환으로 바깥원의 둘레를 따라 눈금표식을 새기고 5min마다 수자들을 새겨넣는다. 본문은 눈금표식아래의 보이지 않는 직4각형안에 넣는다. 한번 순환의 끝에서 그리기장치를 1min에 대응하는 량인 7°씩 시계바늘방향으로 회전한다.

drawLine()과 drawText()호출에 넘기는 자리표들이 늘 같다할지라도 다음에 눈금표식을 그릴 때 원둘레의 각이한 위치에 있게 된다.

로시계를 실현하는 또 하나의 방법은 sin()과 cos()를 리용하여 (x, y)위치를 자체로 계산하여 원둘레에서의 위치들을 찾는것이다. 그러나 그때 여전히 변환과 회전을 리용하여 어떤 각도로 본문을 그릴수 있다.

한가지 문제는 10s마다 창문부분품전체를 다시 그리기하는데 그때마다 깜빡거림이 발생하는것이다. 해결방안은 2중완충기능을 추가하는것이다. 2중완충은 WNoAutoErase를 기초클라스구성자에 넘기고 처음에 보여준 paintEvent()함수를 다음것과 교체하여 수행할수 있다.

void OvenTimer::paintEvent(QPaintEvent *event) {

static QPixmap pixmap;

QRect rect = event→rect();

QSize newSize = rect.size().expandedTo(pixmap.size());

pixmap.resize(newSize);

pixmap.fill(this, rect.topLeft());

QPainter painter(&pixmap, this);

int side = QMIN(width(), height());

painter.setViewport((width() -side) / 2 -event→rect().x(),

(height() -side) / 2 -event→rect().y(), side, side);

painter.setWindow(-50, -50, 100, 100);

draw(&painter);

bitBlt(this, event→rect().topLeft(), &pixmap);

}

그리기경로는 기본그림요소(직4각형, 타원, 직선, 곡선 등)로 이루어진다. 그리기경로는 4각형이나 원과 같이 닫긴 경로일수도 있고 직선이나 곡선과 같이 닫기지 않은 경로일수도 있다.

Qt에서 그리기경로는 QPainterPath클라스를 리용하여 표시한다. 이것은 그리기조작의 용기를 제공하며 이전에 그린 도형을 다시 리용할수 있게 한다.

그리기경로클라스는 채우기, 륜곽현시, 자르기를 할수 있다.

체우기할수 있는 륜곽의 그리기경로를 만들려면 QPainterPathStroker클라스를 리용하여야 한다.

QPainterPath를 리용하면 복잡한 도형을 한번만 만들고 필요한 경우에는 이것을 다시 리용할수 있다.

QPainterPath대상은 시작점만 있는 빈 경로일수도 있고 다른QPainterPath대상으로부터 복사한것일수도 있다. QPainterPath대상을 만든 다음 lineTo(), arcTo(), quadTo()함수를 리용하여 직선과 곡선을 이 경로안에 삽입할수 있다.

직선과 곡선은 currentPosition()에 의하여 얻어지는 점으로부터 그리기를 시작한다.

currentPosition()은 언제나 마지막 부분경로그리기의 끝점을 되돌린다. moveTo()함수는 경로를 첨가하지 않고 currentPosition()을 이동시킬수 있다. 이것은 하나의 부분경로를 닫고 새로운 부분경로그리기를 시작한다. closeSubPath()는 현재의 부분경로를 닫는데 이때 한개의 직선을 리용하여 currentPosition()으로부터 그리기경로의 시작점을 련결시킨다.

QPainter는 addEllipse(), addPath(), addRect(), addRegion(), addText()를 리용하여 기본그림요소들을 그리기경로에 첨가할수 있다. 이미 있던 그리기경로는 connectPath()함수를 리용하여 다른 그리기경로에 첨가할수 있다.

다음의 코드는 QPainterPath를 리용하여 한개의 화살표를 그린다.

QPainterPath path;

path.moveTo(10, 100);

path.cubicTo(10, 100, 100, 10, 200, 70);

path.lineTo(200, 50); path.lineTo(220, 80);

path.lineTo(200, 110); path.lineTo(200, 90);

path.cubicTo(200, 100, 100, 50, 50, 100);

QPainter painter(this);

QPen pen(QColor(255, 0, 0), 2);

painter.setPen(pen);

painter.drawPath(path);

Qt는 두가지 경로채움방식(Qt::OddEvenFill과 Qt::WindingFill)을 제공한다.

Qt::OddEvenFill는 기정채우기방식으로서 QPainterPath가 홀수짝수채우기방식을 리용할것을 지정한다. 이 규칙에서 하나의 점이 경로도형안에 있는가를 판단하는 방법이 있다. 이 방법에서는 한개의 수평선을 이 점으로부터 경로도형외부까지 그어 수평선과 경로의 사귐점수를 제한하여 홀수이면 이 점이 경로안에 있다고 판단한다.

QPainterPath에는 경로의 정보를 얻을수 있는 함수들이 있다.

실례로 elementAt()함수는 지정한 부분경로의 원소를 얻고 isEmpty()함수는 현재의 경로가 빈것인가를 판단한다. 그리고 controlPointRect()함수는 경로안에 있는 모든 점과 조종점으로 이루어진 4각형을 얻는데 이 함수는 정확한 포함테두리를 되돌리는boundingRect()함수보다 실행속도가 훨씬 빠르다.

또한 contains()함수는 한개의 점 또는 4각형이 경로안에 있는가를 판단하며 intersects()함수는 지정한 4각형과 경로가 서로 사귀는가를 판단한다.

QPainterPath는 4각형도형을 다른 도형으로 변환시킬수 있다. 실례로 toFillPolygon(), toFillPolygons(), toSubpathPolygons()함수를 리용하면 경로를 다변형으로 변환시킬수 있다.

QPainterPath는 문자를 경로로 리용할수 있다.

다음의 코드는 선형점변채움을 리용하여 문자경로를 현시한다.

QLinearGradient linearGrad(QPointF(200, 0), QPointF(1000, 0));

linearGrad.setColorAt(0, Qt::black);

linearGrad.setColorAt(1, Qt::white);

QFont font(“청봉”, 80);

font.setBold(true);

QPainterPath textPath;

textPath.addTTText(200, 300, font, tr(“도형처리”));

painter.setBrush(linearGrad);

painter.drawPath(textPath);

### 2. QCanvas에 의한 도형처리

QCanvas는 QPainter가 제공하는것보다 도형처리를 수행하기 위한 더 고급한 대면부를 제공한다. QCanvas는 임의의 형태의 항목들을 포함하며 내적으로 2중완충을 리용하여깜빡거림을 피한다.

자료시각화프로그람들과 2차원유희와 같이 사용자가 조작할수 있는 항목들을 표시할 필요가 있는 응용프로그람들에서 QCanvas의 사용은 QWidget:: paintEvent()나 QScrollView::drawContents()를 재정의하고 모든것을 수동적으로 다시 그리는것보다 더 좋은 수법이다.

QCanvas에 보여준 항목들은 QCanvasItem이나 그 파생클라스의 실례들이다. Qt는 미리 정의된 파생클라스들의 모임을 제공한다. 즉 QCanvasLine, QCanvasRectangle, QCanvasPolygon, QCanvasPolygonalItem, QCanvasEllipse, QCanvasSpline, QCanvasSprite, QCanvasText들을 제공한다. 이 클라스들은 그 자체가 사용자정의그리기항목들을 제공하는 파생클라스로 만들수 있다. QCanvas와 그의 QCanvasItem들은 순수 자료이며 시각적표시를 가지지 않는다. 그림그리기창과 그 항목들을 표시하려면 QCanvasView창문부분품을 사용해야 한다. 이와 같이 자료와 그 시각적표시의 분리는 같은 그림그리기창을 시각화하는 여러개의 QCanvasView창문부분품들을 가질수 있게 한다. 매개의 QCanvasView는 될수록 각이한 변환행렬을 가지고 그림그리기창의 자기 부분을 표시할수 있다.

QCanvas는 대량의 항목들을 처리하도록 고도로 최적화되여있다. 항목이 달라질 때 QCanvas는 달라진 부분을 다시 그린다. 또한 효과적인 충돌탐색알고리듬을 제공한다.

QCanvas사용법을 보여주기 위하여 작은 도표편집기인 DiagramView창문부분품의 코드를 제시한다. 창문부분품은 2개 종류의 도형(직4각형칸과 직선)을 유지하며 사용자가 새로운 직4각형과 직선들을 추가하고 그것들을 복사하고 붙이기하고 삭제하며 그 속성들을 편집하게 하는 문맥차림표를 제공한다.

DiagramView클라스는 QCanvasView를 계승하며 QCanvasView는 QScrollView을 계승한다. 이 클라스는 응용프로그람이 련결할수 있는 많은 공개처리부들을 제공한다. 처리부들은 또한 창문부분품이 자체로 문맥차림표를 실현하는데 사용된다.

DiagramView클라스중에서 2개의 사용자정의그림그리기항목클라스들을 정의하여 그리려고 하는 도형들을 표시한다. 이 클라스들의 이름은 DiagramBox와 DiagramLine이다.

DiagramBox클라스는 직4각형과 본문의 부분을 현시하는 canvas항목의 형이다. 이 클라스는 직4각형을 현시하는 QCanvasItem의 파생클라스 QCanvasRectangle로부터 그 기능을 계승한다. QCanvasRectangle에 직4각형의 중간에 본문을 표시하는 능력과 매개 구석에 아주 작은 바른4각형(《손잡이》)을 표시하고 항목이 능동이라는것을 가리키는 능력을 추가한다. 현실세계의 응용프로그람에서는 손잡이를 찰칵하고 끌어서 칸의 크기를 조절할수 있게 하지만 여기서는 코드를 간단하게 만든다.

rtti()함수는 QCanvasItem로부터 재정의된다. C++의 dynamic_cast<T>()기구에 의하여 같은 검사를 할수 있으나 그 기능을 유지하는 C++콤파일러들에 제한된다.

1001값은 임의로 취한것이다. 1000이상의 값을 받아들일수 있다. 이 값은 같은 응용프로그람에서 사용한 다른 항목형들과 혼돈하지 말아야 한다.

DiagramLine클라스는 직선을 표시하는 그림그리기항목이다. 이 클라스는 QCanvas Line로부터 기능을 계승하며 량끝에 손잡이들을 표시하는 능력을 추가하여 직선이 능동이라는것을 가리킨다.

DiagramView::DiagramView(QCanvas *canvas, QWidget *parent, const char *name):

QCanvasView(canvas, parent, name) {

pendingItem = 0; activeItem = 0;

minZ = 0; maxZ = 0;

createActions();

}

DiagramView구성자는 첫 인수로서 canvas를 가지며 그것을 기초클라스구성자에 넘긴다. DiagramView는 이 그림그리기창을 표시한다.

QAction들은 createActions()비공개함수에서 창조된다.

void DiagramView::contentsContextMenuEvent(QContextMenuEvent *event){

QPopupMenu contextMenu(this);

if (activeItem) {

cutAct→addTo(&contextMenu); copyAct→addTo(&contextMenu);

deleteAct→addTo(&contextMenu);

contextMenu.insertSeparator();

bringToFrontAct→addTo(&contextMenu);

sendToBackAct→addTo(&contextMenu);

contextMenu.insertSeparator();

propertiesAct→addTo(&contextMenu);

} else {

pasteAct→addTo(&contextMenu);

contextMenu.insertSeparator();

addBoxAct→addTo(&contextMenu); addLineAct→addTo(&contextMenu);

}

contextMenu.exec(event→globalPos());

}

contentsContextMenuEvent()함수는 QScrollView로부터 재정의되여 문맥차림표를 창조한다.

항목이 능동이면 차림표는 항목에서 의미를 가지는 작용들 즉 Cut, Copy, Delete, Bring to Front, Send to Back, Properties들로 채워진다. 그렇지 않으면 차림표는 Paste, Add Box, Add Line으로 채워진다.

void DiagramView::addBox() { addItem(new DiagramBox(canvas())); }

void DiagramView::addLine() { addItem(new DiagramLine(canvas())); }

void DiagramView::addItem(QCanvasItem *item) {

delete pendingItem;

pendingItem = item;

setActiveItem(0);

setCursor(crossCursor);

}

addItem()비공개함수는 마우스지시자를 +마우스지시자로 바꾸고 pendingItem을 새로 창조된 항목으로 설정한다. 항목은 show()를 호출하기 전에는 그림그리기창에서 보이지 않는다.

사용자가 문맥차림표로부터 Add Box나 Add Line을 선택하면 마우스지시자는 +마우스지시자로 달라진다. 항목은 사용자가 그림그리기창우에서 찰칵할 때까지 실제로 추가되지 않는다.

void DiagramView::contentsMousePressEvent(QMouseEvent *event) {

if (event→button() == LeftButton && pendingItem) {

pendingItem→move(event→pos().x(), event→pos().y());

showNewItem(pendingItem);

pendingItem = 0;

unsetCursor();

} else {

QCanvasItemList items = canvas()→collisions(event→pos());

if (items.empty())

setActiveItem(0);

else

setActiveItem(*items.begin());

}

lastPos = event→pos();

}

마우스지시자가 +일 때 사용자가 왼쪽마우스단추를 찰칵하면 직4각형이나 직선을 창조할것을 요구하며 새 항목을 표시하려는 위치에서 그림그리기창을 찰칵한다. 항목을 찰칵한 위치에 직4각형이나 선분을 새로 표시하고 마우스지시자를 표준화살마우스지시자로 재설정한다.

그림그리기창에 대한 다른 마우스누르기사건은 항목을 선택하거나 선택을 해제하려는 시도로 해석된다. 그림그리기창에 대하여 collisions()를 호출하여 마우스지시자아래의 모든 항목들을 얻고 첫 항목을 현재 항목으로 만든다. 목록이 많은 항목을 포함하면 첫 항목은 항상 다른 항목들의 꼭대기에 그려지는 항목이다.

void DiagramView::contentsMouseMoveEvent(QMouseEvent *event) {

if (event→state() & LeftButton) {

if (activeItem) {

activeItem→moveBy(event→pos().x()-lastPos.x(),event→pos().y()- lastPos.y());

lastPos = event→pos();

canvas()→update();

}

}

}

사용자는 항목우에서 왼쪽마우스단추를 누르고 끌기하여 항목을 canvas우에서 옮길수 있다. 마우스이동사건을 얻을 때마다 마우스가 이동한 수평 및 수직거리만큼 항목을 옮기고 그림그리기창에 대하여 update()를 호출한다.

void DiagramView::contentsMouseDoubleClickEvent(QMouseEvent *event) {

if (event→button() == LeftButton && activeItem &&

activeItem→rtti() == DiagramBox::RTTI) {

DiagramBox *box = (DiagramBox *)activeItem;

bool ok;

QString newText = QInputDialog::getText(tr("Diagram"), tr("Enter new text:"),

QLineEdit::Normal, box→text(), &ok, this);

if (ok) {

box→setText(newText);

canvas()→update();

}

}

}

사용자가 항목을 두번 찰칵하면 항목의 rtti()함수를 호출하고 그 돌림값을 DiagramBox::RTTI(1001로 정의됨.)와 비교한다.

항목이 DiagramBox이면 QInputDialog를 펼치고 사용자가 칸에 표시되는 본문을 변경하게 한다. QInputDialog클라스는 표식자, 행편집기, OK단추, Cancel단추를 각각 하나씩 제공한다.

void DiagramView::bringToFront(){

if (activeItem) {

++maxZ;

activeItem→setZ(maxZ);

canvas()→update();

}

}

2개 항목이 같은 (x, y)위치를 차지할 때 제일 큰 z값을 가지는 항목을 제일 앞에 표시한다.(z값이 같으면 QCanvas는 항목지적자들의 값에 따라 겹쳐놓는다.)

void DiagramView::sendToBack() {

if (activeItem) {

--minZ;

activeItem→setZ(minZ);

canvas()→update();

}

}

sendToBack()처리부는 그림그리기창에서 현재 능동인 항목을 다른 모든 항목들의 뒤에 넣는다. 이것은 그 항목의 z자리표를 다른 항목들의 z값보다 작은 값으로 설정하여 수행한다.

QRect DiagramBox::boundingRect() const {

return QRect((int)x()-Margin, (int)y()-Margin, width()+2*Margin,

height()+2*Margin);

}

boundingRect()함수는 QCanvasItem으로부터 재정의된다. QCanvas에서는 이 함수를 충돌탐색과 그리기최적화에 리용한다. 함수가 돌려주는 직4각형은 적어도 drawShape()에서 그리는 령역만큼 커야 한다.

### 3. Graphics View에 의한 도형처리

Graphics View는 보기구조의 도형관리모형을 리용하여 대량의 그림요소를 관리할수 있게 하며 충돌검출, 자리표변환과 그림요소묶음과 같은 편리한 기능들을 지원한다. Graphics View는 사건전파체계구조를 지원하고있으며 그림요소들이 무대(scene)안에서 한배 높아진 정확한 교환능력을 가지도록 한다. 그림요소로는 건반건, 마우스의 누르기, 이동, 놓기와 두번 누르기의 사건을 처리할수 있고 마우스의 이동을 추적할수 있다. 또한 Graphics View체계안에서 2진공간분할(BSP:Binary Space Partitioning)을 리용한 빠른 그림요소탐색기능을 제공하여 용량이 큰 무대를 실시간적으로 현시할수 있게 하며 지어는 백만개이상의 그림요소들의 관리를 할수 있게 한다.

Graphics View체계는 QT InterView와 류사한 모형인 그림요소에 기초한 모형(보기프로그람작성구조)을 제공한다. 여기서 처리되는 자료는 도형이다. Graphics View체계는 3개의 기본클라스(QGraphicsScene, QGraphicsView, QGraphicsItem)를 포함하는데 이것은 각각 무대, 보기, 그림요소를 가리킨다. 하나의 무대는 여러개의 보기로 이루어질수 있다. 하나의 무대는 여러개의 기하도형을 포함한다.

QGraphicsScene클라스는 Graphics View안의 무대에 필요한 기능을 제공한다. 무대는 QGraphicsItem객체의 용기이다.

함수 QGraphicsScene::addItem()을 리용하면 그림요소를 무대에 첨가할수 있다. 그림요소는 여러개의 함수를 리용하여 검색할수 있다.

QGraphicsScene::items()와 일부 재적재함수들은 점, 직4각형, 다변형, 벡토르경로와 사귀는 모든 그림요소들을 되돌려준다. QGraphicsScene::itemAt()는 지정한 점의 정점그림요소를 되돌려준다.

QGraphicsScene의 사건전달체계구조는 발생한 무대사건을 그림요소에 넘겨주는것과 함께 그림요소들사이의 사건전달을 관리한다. 만일 무대가 어느 한 점에서의 마우스누르기사건을 접수하면 무대는 이 사건을 이 점위치의 그림요소에 넘겨준다.

QGraphicsScene은 그림요소선택과 초점 등 그림요소들의 상태를 관리한다.

QGraphicsScene::setSelectionArea()함수는 그림요소를 선택하거나 임의의 모양을 가지는 구역을 선택하는데 리용한다. 이때 얻은 그림요소는 QPainterPath를 리용하여 표시할수 있다. 현재 선택된 그림요소배렬을 얻으려면 QGraphicsScene::selectedItems()함수를 리용하여야 한다.

QGraphicsScene은 또한 그림요소의 건반입력초점상태를 관리한다.

QGraphicsScene::setFocusItem()함수와 QGraphicsItem::setFocus()함수는 그림요소의 초점을 설정한다. 현재 초점을 가진 그림요소를 얻으려면 QGraphicsScene:: focusItem()함수를 리용하여야 한다. 무대내용을 특정한 그리기장치에 그리려면 QGraphicsScene::render()함수를 리용하여야 한다.

QGraphicsView는 보기창문부분품으로서 무대의 내용을 현시한다. 이것은 여러개의 보기를 하나의 무대에 련결할수 있는데 같은 자료모임에 서로 다른 여러가지 종류의 보기창문을 제공한다.

QGraphicsView는 흘림이 가능한 창문부분품이다. 흘림띠를 리용하면 큰 무대를 볼수 있다.

보기는 건반이나 마우스의 입력사건을 받아 무대사건으로 변환(자리표를 무대의 자리표로 변환)한다. 변환행렬함수 QGraphicsView::matrix()를 리용하여 무대의 자리표를 변환할수 있다. 이러한 방법을 리용하면 무대의 압축확대나 회전을 실현할수 있다. QGraphicsView에서는 무대의 자리표와의 변환을 진행하는데 QGraphicsView:: mapToScene()과 QGraphicsView::mapFromScene()를 리용한다.

QGraphicsItem은 그림요소기초클라스이다. QGraphicsView체계는 직4각형(QGraphicsRectItem), 타원(QGraphicsEllipseItem), 본문그림요소(QGraphicsTextItem)와 같은 몇가지 표준적인 그림요소들을 제공한다. 리용자는 QGraphicsItem을 계승하여 자기의 요구에 맞는 그림요소를 만들수 있다.

QGraphicsItem은 다음과 같은 기능을 가지고 있다.

마우스의 누르기, 이동, 놓기, 두번 누르기, 끌기, 굴개굴리기, 오른쪽단추차림표사건, 건반입력사건, 끌어다놓기사건처리를 진행하며 묶음으로 가르기와 충돌검출을 진행한다.

그림요소는 자기의 자리표체계를 가지고있는데 무대와 그림요소, 그림과 그림요소사이의 자리표변환함수를 제공한다. 그림요소는 QGraphicsItem::matrix()를 리용하여 자기자체를 변환시킬수 있다. 그림요소는 부분그림요소를 포함할수 있다.

QGraphicsView에서 QGraphicsView::setMatrix()함수는 QPainter와 같은 기하변환기능을 지원한다. QGraphicsView에서 보기변환을 진행할 때 보기의 중심은 변하지 않는다. 변환을 응용하여 쉽게 확대와 축소 및 회전을 진행할수 있다.

신호처리부를 autoRepeat속성을 가진 QToolButton과 련결하면 련속적인 확대축소조작을 진행할수 있다.

Graphics View는 몇가지 서로 다른 준위의 동화를 지원한다. 동화경로는 QGraphicsItem Animation함수를 리용하여 그림요소와 련결할수 있다. 이렇게 하면 시간적으로 선형조종되는 그림요소가 모든 가동환경에서 일정한 속도로 동작하게 된다. QGraphicsItemAnimation은 그림요소의 경로를 만들수 있게 하는데 여기에는 위치, 회전, 확대축소, 비틀기, 평행이동 등 조작경로들이 포함된다. 즉 서로 다른 시각에 서로 다른 변환을 진행한다. 동화는 보통 QTimeLine을 리용하여 조종하며 QSlider를 리용하여서도 조종할수 있다.

그림요소는 QObject와 QGraphicsItem으로부터 계승하여 만들수 있는데 이 클라스의 그림요소는 자기의 계수기를 설정할수 있다.

QObject::timerEvent()를 리용하여 동화의 조종을 진행할수도 있다.

다음의 코드는 태양이 솟는 과정과 지는 과정을 보여준다.

#include <QtGui>

#include <cmath>

using namespace std;

const qreal PI = 3.14159265;

int main(int argc, char* argv[]) {

QApplication app(argc, argv);

QGraphicsEllipseItem *sun = new QGraphicsEllipseItem(0, 0, 20, 20);

sun→setBrush(Qt::red); sun→setPen(QPen(Qt::red));

QTimeLine *timeline = new QTimeLine(10000);

timeline→setCurveShape(QTimeLine::LineCurve);

QGraphicsItemAnimation *animation = new QGraphicsItemAnimation;

animation→setItem(sun); animation→setTimeLine(timeline);

qreal x, y;

qreal angle = PI;

for (int i=0; i<=180; ++i) {

x = 200.0*cos(angle); y = 200.0*sin(angle);

animation→setPostAt(i/180.0, QPointF(x, y));

angle += PI/180.0;

}

QGraphicsScene*scene = new QGraphicsScene();

scene→addItem(sun);

QGraphicsView *view = new QGraphicsView(scene);

view→resize(640, 480); view→show();

timeline→start();

return app.exec();

}

이 프로그람에서는 QTimeLine객체를 리용하여 동화를 조종한다.

QTimeLine의 값변화곡선은 QTimeLine::LinearCurve에 설정되여있는데 이에 따라 QTimeLine의 값이 선형적으로 변화된다. 먼저 시간구간을 180걸음으로 나누어 매 걸음에서 타원의 위치를 설정한다. 다음 시간총길이를 10s로 설정하고 동화를 시작한다. 프로그람은 태양이 반타원의 자리길을 따라 운동하는 과정을 보여준다.

### 4. OpenGL에 의한 도형처리

OpenGL은 2차원과 3차원도형처리를 위한 표준API이다. Qt응용프로그람들은 Qt의 QGL모듈을 리용하여 OpenGL도형을 그릴수 있다.

Qt응용프로그람으로부터 OpenGL에 의한 도형처리는 간단하다. QGLWidget의 파생클라스를 만들고 가상함수들을 재정의하고 응용프로그람을 QGL과 OpenGL서고들에 련결하여야 한다. QGLWidget가 QWidget로부터 계승되므로 이미 알고있는것의 대부분을 여전히 적용할수 있다. 주요한 차이는 표준 OpenGL함수들을 사용하여 QPainter대신에 그리기를 수행한다는것이다.

Cube응용프로그람은 서로 다른 색의 면을 가지는 3차원 정6면체를 표시한다. 사용자는 마우스단추를 누르고 끌기하여 립방체를 회전시킬수 있다. 사용자는 립방체의 한 면을 두번 찰칵하여 펼쳐지는 QColorDialog로부터 색을 선택하여 면의 색을 설정할수 있다.

Cube는 QGLWidget를 계승한다. initializeGL(), resizeGL(), paintGL()함수들은 QGLWidget로부터 재정의된다. 마우스사건처리함수들은 보통과 같이 QWidget로부터 재정의된다. QGLWidget는 <qgl.h>에서 정의된다.

Cube::Cube(QWidget *parent, const char *name) : QGLWidget(parent, name) {

setFormat(QGLFormat(DoubleBuffer | DepthBuffer));

rotationX = 0; rotationY = 0; rotationZ = 0;

faceColors[0] = red; faceColors[1] = green;

faceColors[2] = blue; faceColors[3] = cyan;

faceColors[4] = yellow; faceColors[5] = magenta;

}

구성자에서는 QGLWidget::setFormat()를 호출하여 OpenGL현시문맥을 지정하고 클라스의 비공개변수들을 초기화한다.

void Cube::initializeGL() {

qglClearColor(black); glShadeModel(GL_FLAT);

glEnable(GL_DEPTH_TEST); glEnable(GL_CULL_FACE);

}

initializeGL()함수는 paintGL()이 호출되기 전에 한번 호출된다. 이것은 OpenGL묘사문맥을 설정하고 현시목록을 정의하며 다른 초기화를 수행한다.

모든 코드는 QGLWidget의 qglClearColor()함수호출을 제외하고는 표준 OpenGL이다. 표준 OpenGL로 고착시키려고 한다면 RGBA방식에서는 glClearColor()를, 색첨수방식에서는 glClearIndex()를 각각 대신에 호출한다.

void Cube::resizeGL(int width, int height){

glViewport(0, 0, width, height);

glMatrixMode(GL_PROJECTION);

glLoadIdentity();

GLfloat x = (GLfloat)width / height;

glFrustum(-x, x, -1.0, 1.0, 4.0, 15.0);

glMatrixMode(GL_MODELVIEW);

}

resizeGL()함수는 paintGL()이 처음으로 호출되기 전에 그러나 initializeGL()이 호출된 후에 한번 더 호출된다. 이것은 창문부분품의 크기에 따라 OpenGL보기구역, 사영, 다른 환경을 설정할수 있는 위치이다.

void Cube::paintGL(){

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

draw();

}

paintGL()함수는 창문부분품을 다시 그려야 할 때마다 호출된다. 이것은 QWidget:: paintEvent()와 비슷하지만 QPainter함수들대신에 OpenGL함수들을 사용한다. 실제의 그리기는 비공개함수 draw()에 의해 수행된다.

void Cube::draw()

{

static const GLfloat coords[6] [4] [3] = {

{{+1.0, -1.0, +1.0 }, {+1.0, -1.0, -1.0}, {+1.0, +1.0, -1.0}, {+1.0, +1.0, +1.0}}, {{-1.0, -1.0, -1.0}, {-1.0, -1.0, +1.0}, {-1.0, +1.0, +1.0}, {-1.0, +1.0, -1.0}}, {{+1.0, -1.0, -1.0}, {-1.0, -1.0, -1.0}, {-1.0, +1.0, -1.0}, {+1.0, +1.0, -1.0}}, {{-1.0, -1.0, +1.0}, {+1.0, -1.0, +1.0}, {+1.0, +1.0, +1.0}, {-1.0, +1.0, +1.0}}, {{-1.0, -1.0, -1.0}, {+1.0, -1.0, -1.0}, {+1.0, -1.0, +1.0}, {-1.0, -1.0, +1.0}}, {{-1.0, +1.0, +1.0}, {+1.0, +1.0, +1.0}, {+1.0, +1.0, -1.0}, {-1.0, +1.0, -1.0}}};

glMatrixMode(GL_MODELVIEW);

glLoadIdentity();

glTranslatef(0.0, 0.0, -10.0);

glRotatef(rotationX, 1.0, 0.0, 0.0); glRotatef(rotationY, 0.0, 1.0, 0.0);

glRotatef(rotationZ, 0.0, 0.0, 1.0);

for (int i = 0; i < 6; ++i) {

glLoadName(i);

glBegin(GL_QUADS);

qglColor(faceColors[i]);

for (int j = 0; j < 4; ++j) {

glVertex3f(coords[i][j][0], coords[i][j][1], coords[i][j][2]);

}

glEnd();

}

}

draw()에서는 x, y, z회전 그리고 faceColors배렬에 보관된 색들을 고려하여 직6면체를 그린다. qglColor()호출을 제외한 모든것이 표준 OpenGL이다. 방식에 따라서 OpenGL함수들인 glColor3d() 혹은 glIndex()중 하나를 사용하였다.

void Cube::mousePressEvent(QMouseEvent *event) { lastPos = event→pos(); }

void Cube::mouseMoveEvent(QMouseEvent *event) {

GLfloat dx = (GLfloat) (event→x() -lastPos.x()) / width();

GLfloat dy = (GLfloat) (event→y() -lastPos.y()) / height();

if (event→state() & LeftButton) {

rotationX += 180 * dy; rotationY += 180 * dx;

updateGL();

} else if (event→state() & RightButton) {

rotationX += 180 * dy; rotationZ += 180 * dx;

updateGL();

}

lastPos = event→pos();

}

mousePressEvent()와 mouseMoveEvent()함수들을 QWidget로부터 재정의하여 사용자가 보기를 찰칵하고 끌기하여 회전할수 있게 한다. 왼쪽마우스단추는 사용자가 x와 y축주위로 회전할수 있게 하고 오른쪽마우스단추는 x와 z축주위를 회전할수 있게 한다.

rotationX, rotationY 혹은 rotationZ변수들을 수정한 다음 updateGL()을 호출하여 배경을 다시 그린다.

void Cube::mouseDoubleClickEvent(QMouseEvent*event) {

int face = faceAtPosition(event→pos());if (face != -1) {

QColor color = QColorDialog::getColor(faceColors[face], this);

if (color.isValid()) {

faceColors[face] = color;

updateGL();

}

}

}

mouseDoubleClickEvent()을 QWidget로부터 재정의하여 사용자가 립방체의 한 면을 두번 찰칵하여 면의 색을 설정하게 한다. 비공개함수 faceAtPosition()를 호출하여 마우스지시자아래에 배치된 립방체면을 결정한다. 한 면을 두번 찰칵하면 QColorDialog:: getColor()를 호출하여 그 면의 새로운 색을 얻는다. 그다음 새로운 색으로 faceColors배렬을 갱신하고 updateGL()를 호출하여 배경을 다시 그린다.

int Cube::faceAtPosition(const QPoint &pos){

const int MaxSize = 512;

GLuint buffer[MaxSize];

GLint viewport[4];

glGetIntegerv(GL_VIEWPORT, viewport);

glSelectBuffer(MaxSize, buffer);

glRenderMode(GL_SELECT);

glInitNames(); glPushName(0);

glMatrixMode(GL_PROJECTION);

glPushMatrix(); glLoadIdentity();

gluPickMatrix((GLdouble)pos.x(), (GLdouble) (viewport[3] -pos.y()), 5.0, 5.0, viewport);

GLfloat x = (GLfloat)width() / height();

glFrustum(-x, x, -1.0, 1.0, 4.0, 15.0);

draw();

glMatrixMode(GL_PROJECTION);

glPopMatrix();

if (!glRenderMode(GL_RENDER))

return -1;

return buffer[3];

}

faceAtPosition()함수는 창문부분품우에서 일정한 위치에 있는 면의 번호를 돌려주며 그 위치에 면이 없으면 –1을 돌려준다. OpenGL에서 이것을 결정하는 코드는 좀 복잡하다. 본질적으로 OpenGL의 포착능력의 우점을 리용하도록 GL_SELECT방식으로 배경을 그리고 OpenGL히트(hit)기록으로부터 면번호(이름)를 얻는다.

main함수는 다음과 같다.

#include <qapplication.h>

#include "cube.h"

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

if (!QGLFormat::hasOpenGL())

qFatal("This system has no OpenGL support");

Cube cube;

cube.setCaption(QObject::tr("Cube")); cube.resize(300, 300);

app.setMainWidget(&cube);

cube.show();

return app.exec();

}

사용자의 체계가 OpenGL을 유지하지 않으면 조종탁에 오유통보문을 출력하고 Qt의 qFatal()대역함수에 의하여 중지한다. 응용프로그람을 QGL 및 OpenGL서고들에 련결할 때 .pro화일이 이 항목을 요구한다.

CONFIG += opengl

이로서 Cube응용프로그람을 끝낸다.

## 제4절. 모형과 보기구조

모형과 보기구조를 리용하여 자료와 표현을 분리하는데 이것을 “InterView framework”라고 부른다. InterView를 리용하면 하나의 모형을 서로 다른 보기구조로 나타낼수 있으며 자료와 보기의 호상변화를 적게 할수 있다.

### 1. MVC설계모형

MVC(Model-View Controller)설계모형은 리용자대면부를 설계할 때 리용한다. MVC에는 3개의 원소가 있다. 모형은 자료를, 보기는 리용자대면부를, 조종은 리용자대면부에서의 조작을 나타낸다. MVC설계모형을 리용하여 자료와 리용자대면부의 분리를 효과적으로 진행한다.

리용자의 입력처리를 더 원만히 하기 위하여 InterView에서는 대리(delegate)를 리용한다. 대리는 자료항목(item)의 현시와 편집방식을 자체정의한다.

그림 2‐2. 모형과 보기구조

Qt의 모형과 보기구조는 3개의 부분(모형, 보기, 대리)으로 나눈다. 보기는 모형에서 모형색인(model index)을 얻으며 모형색인은 자료항목을 인용하는데 리용한다. 보기에서 대리는 자료항목을 그리기하는데 리용한다. 또한 항목을 편집할 때 대리와 모형은 직접통신을 진행한다.

모형, 보기, 대리사이의 통신은 신호와 처리부를 리용하여 진행하는데 그 관계는 다음과 같다.

·자료가 변화될 때 모형은 신호를 보기에 보낸다.

·리용자가 대면부에서 조작할 때 보기는 신호를 발생시킨다.

·대리는 신호를 발생시켜 모형과 보기에 편집기의 현재 상태를 알린다.

모든 모형클라스들은 다 QAbstractItemModel클라스에 기초한다.

QAbstractListModel클라스와 QAbstractTableModel클라스는 목록과 표모형의 추상기초클라스이며 QAbstractProxyModel클라스는 대리모형의 추상클라스이다. 그밖의 클라스들은 직접 리용할수 있는 모형클라스들이다. QDirModel클라스는 화일과 목록의 보관모형을 제공하며 QStringListModel클라스는 QStringList객체를 보관한다.

QSqlQueryModel클라스와 그 자식클라스들은 자료기지조작을 한다.

InterView framework의 모든 보기클라스들은 모두 추상기초클라스 QAbstractItemView로부터 계승된다.

Qt에는 5개의 기본적인 보기클라스, 3개의 Widget클라스 등이 있다. 여기서 클라스 QTreeWidget, QListWidget, QTableWidget는 자료를 이미 가지고있으면서 모형과 보기를 하나로 통합한 클라스들이다.

InterView framework에서 대리클라스들은 QAbstractItemDelegate추상클라스에 기초한다. 여기에는 QItemDelegate클라스와 QSqlRelationDelegate클라스가 있다. QSqlRelationalDelegate클라스는 자료기지에서 자료를 편집하고 현시하는 관계대리클라스이다. 만일 항목의 편집과 현시를 변화시키려면 반드시 자기의 대리클라스를 정의해야 한다. 자체정의한 클라스는 보기에서 큰 변화를 줄 때에만 필요하다.

### 2. 모형 및 보기클라스의 리용

#### 1) 모형클라스와 보기클라스

InterView framework의 모형클라스들과 보기클라스들은 일반적으로 많이 리용된다. 모형클라스들에는 QStandardItemModel, QDirModel, QStringListModel이 있으며 보기클라스들에는 QColumnView, QHeaderView, QListView, QTableView, QTreeView가 있다.

QDirModel클라스와 QTreeView클라스를 리용한 목록열람프로그람은 다음과 같다.

DirWidget클라스에서는 QTreeView객체와 QLineEdit객체를 정의한다.

QCompleter클라스는 자동완성클라스이다. 이것은 리용자가 경로를 입력하면 내용을 자동적으로 현시한다.

구성자함수의 코드는 다음과 같다.

DirWidget::DirWidget() {

model = new QDirModel;

tree = new QTreeView;

tree→setModel(model);

index = model→index(QDir::currentPath());

tree→expand(index); tree→scrollTo(index);

tree→header()→setResizeMode(QHeaderView::ResizeToContents);

completer = new QCompleter(this);

completer→setModel(model);

dirEdit = new QLineEdit;

dirEdit→setCompleter(completer);

connect(dirEdit, SIGNAL(editingFinished()), this, SLOT(pathChanged()));

layout = new QVBoxLayout;

layout→addWidget(tree); layout→addWidget(dirEdit);

setLayout(layout);

resize(640, 480);

setWindowTitle(QObject::tr(“Dir View”));

}

구성자함수에서는 먼저 현재 목록경로를 얻고 QTreeView의 expand()함수를 리용하여 현재 목록을 현시한다. 또한 scrollTo()함수를 리용하여 scroll을 현재 목록까지 이동시킨다. 다음 setResizeMode(QHeaderView::ResizeToContents)함수를 리용하여 나무구조보기의 현시공간을 충분히 넓혀 완전한 목록이름을 볼수 있게 한다.

편집칸 dirEdit객체에 자동완성기능을 설정한다. 자동완성클라스 QCompleter도 모형에 기초한 클라스이다. 그러나 여기서는 QDirModel을 리용한다. 이렇게 하면 편집칸 dirEdit는 리용자가 입력한 목록과 화일을 자동적으로 판단한다. 리용자가 경로를 입력하면 QTreeView를 갱신한다.

void DirWidget::pathChanged() {

index = model→index(dirEdit→text());

tree→expand(index); tree→scrollTo(index);

}

main함수의 코드는 다음과 같다.

#include <QtGui/QApplication>

#include “dirwidget.h”

int main(int argc, char *argv[]) {

QApplication a(argc, argv);

DirWidget w;

w.show();

return a.exec();

}

Qt에는 일반적인 자료모형들을 처리하는 클라스 QListWidget, QTreeWidget, QTableWidget가 있다. 이 클라스들은 모형과 보기를 하나로 결합하여 일반적인 자료모형을 편리하게 처리한다.

QTableWidget클라스를 리용한 프로그람에서는 Qt의 Undo framework를 리용하여 편집과 형식설정의 undo조작과 redo조작을 실현한다. Undo framework는 undo조작과 redo조작을 실현하는 일반적인 framework이다. 이 framework를 리용하면 많은 코드량을 줄일수 있다.

먼저 QTableWidget클라스에서 계승되는 UndoWidget클라스를 정의한다. 이 클라스는 표에서 임의의 칸의 전경색, 배경색, 서체의 수정, undo조작, redo조작을 실현한다.

UndoStack는 Undo framework가 제공하는 undo조작과 redo조작내용을 보관하는 탄창객체이다. QUndoStack는 QUndoCommand객체를 보관하며 push함수를 리용하여 QUndoCommand명령을 탄창에 넣는다. 다음 undo()함수와 redo()함수로 undo조작과 redo조작을 실현한다. 이를 위하여 표를 초기화하고 신호와 처리부의 련결을 진행한다.

#### 2) 모형색인

모형은 보기와 대리에 표준대면부를 제공한다. Qt의 모형들은 모두 QAbstractItemModel에 기초하여 파생된다. 자료가 변화될 때 모형은 신호를 보기에 보낸다.

InterView는 자료의 보관과 표시의 분리를 보장하기 위하여 모형색인(Model Index)을 리용한다. 모형색인을 리용하여 자료항목을 보관하는데 여기에는 반드시 3개의 속성(행번호, 렬번호, 부모항목의 모형색인)이 있어야 한다.

모형색인에는 다음과 같은 구조방식이 있다.

·표모형색인(table model index)은 행과 렬을 지정해주면 임의의 원소의 위치를 확정한다.

·목록모형색인(list model index)은 렬만 지정해주면 임의의 원소의 위치를 확정한다.

·나무모형색인(tree model index)에서 제일 웃층의 나무가지마디의 행번호는 차례로 증가하는데 매개 나무가지아래의 같은 층마디의 행번호는 다시 정해주어야 한다. 그렇기때문에 나무모형색인을 보관할 때 행, 렬, 부모색인을 지정해주어야 한다.

모형색인에는 림시색인정보만 있다. 그것은 모형의 내부구조가 변화된 다음에 모형색인을 할수 없기때문이다. 이런 현상을 없애려면 Qt의 QPersistentModelIndex클라스로 모형색인을 보관하여야 한다.

모형에서 항목(Item)은 서로 다른 역할을 하며 서로 다른 상태에서 서로 다른 자료를 제공한다. 례를 들어 Qt::DisplayRole은 보기에서 현시한 문자를 보관하는데 이때 항목의 역할은 렬거형 Qt::ItemDataRole로 정의한다.

례를 들어 표칸에 도구통보정보를 설정하는 명령은 다음과 같다.

Model→setData(index, tr(“tooltip”), Qt::ToolTipRole);

리용자가 정의한 모형을 만들려면 그 모형을 QAbstractItemModel클라스로부터 계승되게 하여야 한다. QAbstractListModel클라스와 QAbstractTableModel클라스로부터 계승되게 목록모형과 표모형을 만들수 있다.

자체정의한 모형을 만들려면 반드시 기초클라스의 순수가상함수와 다른 특정함수들을 만들어야 한다.

수값코드를 문자모형으로 절환하는 프로그람에서 모형은 서로 다른 종류의 책들을 보관한다.

BookModel클라스는 QAbstractTableModel로부터 계승되는데 기본적인 순수가상(pure virtual)함수들인 rowCount(), columnCount(), data(), 표머리자료를 되돌려주는headerData()를 정의한다.

BookModel클라스의 실현화일코드는 다음과 같다.

먼저 표를 초기화하고 자료를 입력한다.

#include <QtGui>

#include “bookmodel.h”

BookModel::BookModel(QObject *parent) : QAbstractTableModel(parent) {

bookKindMap[1] = tr(“mathematics”); bookKindMap[2] = tr(“computer”);

bookKindMap[3] = tr(“physics”); bookKindMap[4] = tr(“English”);

bookMap[1] = tr(“math 1”); bookMap[2] = tr(“math 2”);

bookMap[3] = tr(“IT”); bookMap[4] = tr(“C++”);

bookMap[5] = tr(“physics 3”); bookMap[6] = tr(“physics 1”);

bookMap[7] = tr(“Eng 1”); bookMap[8] = tr(“Eng 2”);

populateModel();

}

다음 QMap자료구조를 리용하여 수값을 문자로 넘기기한다.

표의 기초자료를 입력하는 populateModel()함수의 코드는 다음과 같다.

void BookModel::populateModel() {

header<<tr(“BookKind”)<<tr(“Book”)<<tr(“Number”);

bookKind<<1<<2<<3<<4<<2<<4<<3<<1;

book<<1<<3<<5<<7<<4<<8<<6<<2;

type<<tr(“100”)<<tr(“150”)<<tr(“120”)<<tr(“80”)<<tr(“50”)<<tr(“200”);

}

int BookModel::columnCount(const QModelIndex& parent) const { return 3; }

int BookModel::rowCount(const QModelIndex& parent) const {

return book.size();

}

QVariant BookModel::data(const QModelIndex &index, int role) const {

if (!index.isValid())

return QVariant();

QDebug()<<index;

if (role==Qt::DisplayRole) {

switch(index.column()) {

case 0:

return bookKindMap[bookKind[index.row()]];

break;

case 1:

return bookMap[book[index.row()]];

break;

case 2:

return type[index.row()];

default:

return QVariant();

}

}

return QVariant();

}

data()함수는 색인을 지정한 자료를 되돌린다. 여기서는 수값을 문자로 넘기기하여 되돌린다.

QVariant BookModel::headerData(int section, Qt::Orientation orientation, int role) const {

if (role == Qt::DisplayRole && orientation == Qt::Horizontal)

return header[section];

return QAbstractTableModel::headerData(section, orientation, role);

}

headerData()함수는 고정된 표머리자료를 되돌린다. 여기서는 수평표머리자료의 제목만 설정한다.

#include <QtGui>

#include “bookmodel.h”

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

QTextCodec::setCodecForTr(QTextCodec::codecForLocale());

BookModel model;

QTableView view;

view.setModel(&model);

view.setWindowTitle(QObject::tr(“user-defined model”));

view.resize(640, 480); view.show();

return app.exec();

}

#### 3) 대리모형

대리모형(proxy model)은 모형자료의 순서배치, 려과에 리용된다. 대리모형은 모형과 보기사이의 자료처리대리를 리용하여 원천모형과 보기사이의 특수한 자료처리를 진행한다.

Qt는 QSortFilterProxyModel대리모형클라스를 리용하여 순서배치와 려과조작을 완성한다. 자체정의대리모형클라스는 QSortFilterProxyModel클라스에서 계승되여 순서배치와 려과조작을 하며 직접 QAbstractItemModel클라스에서 계승하여 대리모형을 만든다.

려과대리모형을 리용하여 학생들의 시험성적을 려과현시하는 프로그람실례는 다음과 같다.

대면부에서 QTableView객체 tableView를 만들고 이 객체의 sortingEnabled속성을 “true”로 설정하면 표의 자료들이 순서로 배치된다. 대면부에서 매개 QSpinBox객체의 값범위는 모두 0~100이다.

클라스머리부에는 국어(Korean), 수학(Math), 영어(English)성적의 수값범위를 려과하는 filterAcceptsRow()함수가 있다. 이 함수는 려과해야 할 값에 대하여 “false”를 되돌린다.

클라스실현부에서는 먼저 수값범위를 설정하는 6개의 함수를 정의한다.

#include <QtGui>

#include “mysortfilterproxymodel.h”

MySortFilterProxyModel::MySortFilterProxyModel(QObject *parent):QSortFilterProxyModel(parent) {

}

void MySortFilterProxyModel::setMinKorean(const int korean) {

minKorean=korean; invalidateFilter();

}

void MySortFilterProxyModel::setMaxKorean(const int korean) {

maxKorean=korean; invalidateFilter();

}

void MySortFilterProxyModel::setMinMath(const int math) {

minMath=math; invalidateFilter();

}

void MySortFilterProxyModel::setMaxMath(const int math) {

maxMath=math; invalidateFilter();

}

void MySortFilterProxyModel::setMinEnglish(const int english) {

minEnglish=english; invalidateFilter();

}

void MySortFilterProxyModel::setMaxEnglish(const int english) {

maxEnglish=english; invalidateFilter();

}

매개 함수는 모두 invalidateFilter()함수를 호출한다.

이 함수는 려과조건이 이미 변화되였다는것과 대리모형을 갱신하여야 한다는것을 모형에 알리며 filterAcceptsRow()함수를 호출한다.

filterAcceptsRow()함수의 코드는 다음과 같다.

bool MySortFilterProxyModel:: filterAcceptsRow(int sourceRow, const QModelIndex &sourceParent) const {

QModelIndex indexKorean=sourceModel()→index(sourceRow, 1, sourceParent);

QModelIndex indexMath=sourceModel()→index(sourceRow, 2, sourceParent);

QModelIndex indexEnglish=sourceModel()→index(sourceRow, 3, sourceParent);

int korean=sourceModel()→data(indexKorean).toInt();

if (korean<minKorean || korean>maxKorean)

return false;

if (math<minMath || math>maxMath)

return false;

if (english<minEnglish || korean>maxEnglish)

return false;

return true;

}

filterAcceptsRow()함수는 모형의 매개 행에 대한 호출을 진행한다.

매 렬의 값이 려과하려는 수값범위안에 있는가를 판단하는데 조건이 맞으면 “false”를 되돌리며 아니면 “true”를 되돌린다.

#### 4) 자체정의보기

일반적으로 보기(view)는 자료항목대리(item delegate)를 리용하여 만들수 있다.

자체정의한 보기를 만들려면 그것이 QAbstractItemView클라스에서 계승되게 하여야 한다.

QDataWidgetMapper클라스를 리용하여 모형의 어떤 행에서 매 렬의 자료를 창문부분품에 넘기기할수 있으며 특정한 창문부분품이 모형의 자료를 현시하고 편집하게 할수 있다.

여기서 표는 모형에서 넘기기하는 여러가지 창문부분품들(QComboBox, QLineEdit, QDoubleSpinBox, QLabel 등)을 가지고있어야 한다.

QDataWidgetMapper클라스는 자료보고를 위한 2가지 방식을 리용한다.

QDataWidgetMapper::AutoSubmit는 기정방식으로서 자동적으로 수정된 자료를 보관한다.

QDataWidgetMapper::ManualSubmit는 수동보고방식으로서 자료를 수정한 다음 수동적으로 자료수정을 확인한다.

void MapWidget::populateModel() {

model=new QStandardItemModel(3, 3, this);

animals<<tr(“cow”)<<tr(“shark”)<<tr(“pigeon”);

QStringList types;

types<<tr(“animal”)<<tr(“fish”)<<tr(“bird”);

QList<qreal> weights;

weights<<150<<200<<3;

QStandardItem *item;

for (int row=0;row<3;++row){

item=new QStandardItem(animals[row]);

model→setItem(row, 0, item);

item=new QStandardItem(types[row]);

model→setItem(row, 0, item);

model→setData(model→index(row, 2, QModelIndex()), weights[row]);

}

}

대면부갱신함수 updateUI()의 코드는 다음과 같다.

void MapWidget::updateUI(int row){

btnPrev→setEnabled(row>0);

btnNext→setEnabled(row<model→rowCount()-1);

}

자료가 첫 자료인가(또는 마지막 자료인가)를 판단하여 next단추(또는 previous단추)를 리용할수 없게 한다. 자료항목의 대리클라스정의부에서는 setEditorData()함수로 모형의 자료를 QComboBox에 넘기기하며 setModelData()함수로 QComboBox가 선택한 항목을 모형에 넘기기한다.

#include <QtGui>

#include “mapdelegate.h”

MapDelegate::MapDelegate(QObject *parent): QItemDelegate(parent) {

}

void MapDelegate::setEditorData(QWidget *editor, const QModelIndex &index) const {

if(index.column()==0) //company

{

QComboBox *comboEditor=qobject_cast<QComboBox*>(editor);

if(comboEditor){

int i=comboEditor→findText(index.model()→data(index, Qt::EditRole).toString());

comboEditor→setCurrentIndex(i);

}

}

else

return QItemDelegate::setEditorData(editor, index);

}

void MapDelegate::setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const {

if (index.column()==0)

{

QComboBox *comboBox=qobject_cast<QComboBox *>(editor);

if (comboBox)

model→setData(index, comboBox→currentText());

}

else

return QItemDelegate::setModelData(editor, model, index);

}

# 제3장. Qt응용프로그람의 기초기술

## 제1절. 입출력처리

Qt의 QDataStream과 QTextStream클라스들은 화일을 간단히 읽고 쓰게 한다. 이 클라스들은 바이트순서화와 본문부호화와 같은 문제들을 고려하여 각이한 가동환경에서 실행하는 Qt응용프로그람들이 화일들을 읽고 쓸수 있게 한다.

수많은 응용프로그람들은 등록부를 조사하거나 화일에 대한 정보를 얻어야 한다. Qt의 QDir와 QFileInfo클라스들이 이것을 가능하게 한다.

일부 경우에 GUI응용프로그람내에서 외부프로그람들을 실행해야 한다. Qt의 QProcess클라스는 GUI응답성을 유지하면서 외부프로그람들을 신호들과 비동기적으로 실행되게 한다.

### 1. 두값자료의 읽기와 쓰기

QDataStream에 의한 두값자료의 읽기와 쓰기는 Qt에서 사용자정의자료를 적재하고 보관하는 가장 간단한 방법이다. QDataStream은 QByteArray, QFont, QImage, QMap<K, T>, QPixmap, QString, QValueList<T>, QVariant를 비롯한 수많은 Qt자료형들을 유지한다.

두값자료의 취급방법을 보여주기 위하여 2개의 실례클라스 즉 Drawing과 Gallery를 리용한다. Drawing클라스는 그림에 대한 기초정보(저자의 이름, 제목, 창작년도)를 보유하고 Gallery클라스는 Drawing들의 목록을 보관한다.

Gallery클라스는 자료를 보관하고 적재하기 위한 공개함수들을 포함한다. 자료는 drawings자료성원에 보관된 그림들의 목록이다. 비공개함수들은 그것들을 사용할 때 설명한다.

여기에 Gallery의 그림들을 두값자료로 보관하기 위한 간단한 함수가 있다.

bool Gallery::saveBinary(const QString &fileName) {

QFile file(fileName);

if (!file.open(IO_WriteOnly)) {

ioError(file, tr("Cannot open file %1 for writing"));

return false;

}

QDataStream out(&file);

out.setVersion(5);

out << (Q_UINT32)MagicNumber;

writeToStream(out);

if (file.status() != IO_Ok) {

ioError(file, tr("Error writing to file %1"));

return false;

}

return true;

}

화일을 열고 그 화일을 QDataStream의 목표로 만든다. QDataStream의 판을 5로 설정한다. 판번호는 Qt자료형들을 표시하는 방법에 영향을 준다. C++기본자료형들은 늘 같은 방법으로 표시된다.

그다음 Gallery화일형식을 식별하는 수(MagicNumber)를 출력한다. 모든 가동환경에서 수가 32비트옹근수로 씌여진다는것을 담보하기 위하여 수를 정확히 32비트로 만드는 자료형인 Q_UINT32로 강제변환한다.

화일본체는 writeToStream()비공개함수에 의해 써넣어진다. 화일을 정확히 닫을 필요가 없고 이것은 QFile변수가 함수끝에서 리용범위밖으로 벗어날 때 자동적으로 수행된다. writeToStream()호출후에 QFile장치의 상태를 검사한다. 오유가 있으면 ioError()를 호출하여 사용자에게 통보창을 표시하고 false를 돌려준다.

writeToStream()함수는 Gallery의 그림들을 모두 순환하면서 Drawing클라스의 <<연산자에 기초하여 주어진 흐름에 그것들을 출력한다. 그림들을 보관하는데 list<Drawing>대신에 QValueList<Drawing>를 리용한다면 순환을 생략하고 간단히 다음과 같이 쓰면 된다.

out << drawings;

QValueList<T>가 흐름에 흐를 때 목록에 보관된 매개 항목은 항목형의 <<연산자에 의하여 출력된다.

QDataStream &operator<<(QDataStream &out, const Drawing &drawing) {

out << drawing.myTitle << drawing.myArtist << drawing.myYear;

return out;

}

Drawing을 출력하기 위해서는 세개 비공개성원변수들 즉 myTitle, myArtist, myYear를 간단히 출력한다. 그러기 위하여 operator<<()를 Drawing의 동료로서 선언할 필요가 있다. 함수의 끝에서 흐름을 돌려준다. 이것은 C++의 일반적인 관례로서 출력흐름과 함께 여러개의 <<연산자들을 련이어 쓸수 있게 한다.

### 2. 본문의 읽기와 쓰기

Qt는 본문자료를 읽고쓰기 위한 QTextStream클라스를 제공한다. 평본문화일들이나 HTML, XML, 원천화일들과 같은 다른 형식의 화일들을 읽고 쓰는데 QTextStream을 사용할수 있다. 이 클라스는 유니코드와 체계의 국부8비트부호화사이의 변환을 고려하며 서로 다른 조작체계들에서 사용되는 서로 다른 행끝처리를 알기 쉽게 진행한다.

QTextStream은 자료의 기본단위로서 QChar를 사용한다. 문자와 문자렬외에 QTextStream은 C++의 기본수값형을 유지하며 그것들과 문자렬사이를 변환한다.

여기에 Gallery로부터 그림자료들을 보관하는 saveText()함수의 코드가 있다.

bool Gallery::saveText(const QString &fileName) {

QFile file(fileName);

if (!file.open(IO_WriteOnly | IO_Translate)) {

ioError(file, tr("Cannot open file %1 for writing"));

return false;

}

QTextStream out(&file);

out.setEncoding(QTextStream::UnicodeUTF8);

list<Drawing>::const_iterator it = drawings.begin();

while (it != drawings.end()) {

out << *it;

++it;

}

if (file.status() != IO_Ok) {

ioError(file, tr("Error writing to file %1"));

return false;

}

return true;

}

IO_Translate기발을 사용하여 화일을 열 때 새 행문자를 목표가동환경의 정확한 문자렬(Windows에서 "\r\n", Mac OS X에서 "\r")로 변환한다. 그다음 전체 유니코드문자모임을 표시할수 있는 ASCII호환부호화인 UTF-8로 부호화를 설정한다. 출력을 조종하려면 <<연산자에 기초하여 Gallery안의 매개 그림을 순환한다.

QTextStream &operator<<(QTextStream &out, const Drawing &drawing) {

out << drawing.myTitle << ":" << drawing.myArtist << ":"<< drawing.myYear << endl;

return out;

}

그림을 써넣을 때에는 하나의 두점을 리용하여 그림의 제목과 저자의 이름을 분리하고 다른 두점으로 저자의 이름과 년도를 분리하며 새 행으로 자료를 끝낸다. 제목과 저자의 이름은 두점 또는 새 행을 포함하지 않는것으로 가정한다.

bool Gallery::loadText(const QString &fileName) {

QFile file(fileName);

if (!file.open(IO_ReadOnly | IO_Translate)) {

ioError(file, tr("Cannot open file %1 for reading"));

return false;

}

drawings.clear();

QTextStream in(&file);

in.setEncoding(QTextStream::UnicodeUTF8);

while (!in.atEnd()) {

Drawing drawing;

in >> drawing;

drawings.push_back(drawing);

}

if (file.status() != IO_Ok) {

ioError(file, tr("Error reading from file %1"));

return false;

}

return true;

}

흥미있는 부분은 while순환이다. 유효자료가 있는 동안>>연산자에 의하여 읽어들인다. >>연산자의 실현은 그리 간단하지 않다.

out << "alpha" << "bravo";

out가 QTextStream이면 실제로 써넣어지는 자료는 문자렬 "alphabravo"이다. QTextStream에서 읽어들일 때 실제로 이것을 기대할수 없다.

in >> str1 >> str2;

사실상 그때 발생하는 일은 str1의 전체 단어 "alphabravo"를 얻고 str2은 아무것도 없다. QDataStream은 문자자료의 앞에 매개 문자렬의 길이를 보관하므로 문제가 없다.

써넣은 본문이 하나의 단어로 이루어지면 그것들사이에 공백을 넣고 단어별로 자료를 읽을수 있다. 저자의 이름과 그림의 제목은 보통 1개이상의 단어를 포함하므로 그림의 경우에 이것을 수행할수 없다. 그리하여 매개 행을 전부 읽어들이고 그것을 QStringList::split()에 의해 마당들로 분리한다.

QTextStream &operator>>(QTextStream &in, Drawing &drawing) {

QString str = in.readLine();

QStringList fields = QStringList::split(":", str);

if (fields.size() == 3) {

drawing.myTitle = fields[0]; drawing.myArtist = fields[1];

drawing.myYear = fields[2].toInt();

}

return in;

}

QTextStream::read()를 사용하여 한번에 전체 본문을 읽을수 있다.

QString wholeFile = in.read();

결과문자렬에서 매개 행의 끝은 읽어들이는 화일에 의해 사용되는 행마감관례에 관계없이 새 행문자('\n')로 지정된다.

전체 본문화일의 읽기는 자료를 앞처리하여야 하는 경우에 아주 편리하다. 례를 들면

wholeFile.replace("&", "&");

wholeFile.replace("<", "<");

wholeFile.replace(">", ">");

한번에 써넣기 위하여 자료를 모두 하나의 문자렬에 넣고 그것을 한번에 출력한다.

QString Gallery::saveToString(){

QString result;

QTextOStream out(&result);

list<Drawing>::const_iterator it = drawings.begin();

while (it != drawings.end()) {

out << *it;

++it;

}

return result;

}

본문을 화일에 출력하는것처럼 문자렬에 본문을 출력하는것은 간단하며 역시 <<연산자에 기초한다.

void Gallery::readFromString(const QString &data) {

QString string = data;

drawings.clear();

QTextIStream in(&string);

while (!in.atEnd()) {

Drawing drawing;

in >> drawing;

drawings.push_back(drawing);

}

}

QTextStream에 의하여 문자렬에서 자료를 발취하는것은 간단하다. >>연산자에 의거하므로 문장해석은 필요없다.

본문자료의 써넣기는 어렵지 않지만 본문읽기는 잘 되지 않는다. 복잡한 형식에 대해서는 완전확장된 문장해석기가 필요하다. 일반적으로 그러한 문장해석기는 QChar에 대하여 >>에 의해 한 문자씩 자료를 읽어들이거나 readLine()에 의하여 한 행씩 자료를 읽어들이고 돌아온 QString을 순환하면서 작업한다.

### 3. 화일과 등록부의 조종

Qt의 QDir클라스는 등록부를 조사하면서 화일들에 대한 정보를 얻기 위한 가동환경에 의존하지 않는 수단을 제공한다. QDir의 사용방법을 알기 위하여 특정한 등록부와 임의의 깊이의 모든 보조등록부들에서 모든 화상들에 의해 소비되는 공간을 계산하는 자그마한 조작탁응용프로그람을 작성한다.

응용프로그람의 핵심부는 imageSpace()함수로서 주어진 등록부의 크기를 계산한다.

int imageSpace(const QString &path) {

QDir dir(path);

QStringList::Iterator it;

int size = 0;

QStringList files = dir.entryList("*.png *.jpg *.jpeg", QDir::Files);

it = files.begin();

while (it != files.end()) {

size += QFileInfo(path, *it).size();

++it;

}

QStringList dirs = dir.entryList(QDir::Dirs);

it = dirs.begin();

while (it != dirs.end()) {

if (*it != "." && *it != "..")

size += imageSpace(path + "/" + *it);

++it;

}

return size;

}

주어진 경로를 리용하여 QDir객체를 창조하는것으로 시작한다. entryList()함수에 2개의 인수를 넘긴다. 첫째 인수는 공백으로 구분한 화일이름려과기들의 목록이다. 이것들은 대리기호 '*'와 '?'들을 포함한다. 이 실례에서는 오직 PNG와 JPEG화일들만 포함하도록 려과한다. 둘째 인수는 어떤 종류의 항목(보통화일, 등록부, 구동기 등)들을 포함하는가 지정한다.

화일목록을 순환하면서 그 크기를 루계한다. QFileInfo클라스는 화일의 크기, 허가, 소유자, 시간과 같은 속성들을 호출하게 한다.

두번째의 entryList()호출에서 이 등록부의 모든 보조등록부들을 얻고 그것들을 조사하면서 imageSpace()을 재귀호출하여 루계화상크기를 확인한다.

매개 보조등록부의 경로를 창조하기 위해서는 현재 등록부의 경로를 사선으로 구분하여 보조등록부이름(*it)과 결합한다. QDir는 '/'를 모든 가동환경에서 등록부구분기호로서, Windows에서는 '\'를 구분기호로서 취급한다. 사용자에게 경로를 표시할 때 정적함수 QDir::convertSeparators()를 호출하여 사선들을 가동환경에 고유한 정확한 구분기호로 변환한다.

프로그람에 main()함수를 추가한다.

int main(int argc, char *argv[]) {

QString path = QDir::currentDirPath();

if (argc > 1)

path = argv[1];

cerr << "Space used by images in " << endl

<< path.ascii() << endl

<< "and its subdirectories is"<< (imageSpace(path) / 1024) << " KB" << endl;

return 0;

}

이 실례에서는 Qt의 도구클라스들만 사용하므로 QApplication객체를 요구하지 않는다. QDir::currentDirPath()를 사용하여 경로를 현재 등록부로 초기화한다. 또한 QDir:: homeDirPath()를 리용하여 경로를 사용자의 기준등록부로 초기화할수 있다. 사용자가 지령행에 경로를 지정하면 그대신 그것을 사용한다. 끝으로 imageSpace()함수에 의하여 화상들이 소비한 공간을 계산한다.

QDir클라스는 rename(), exists(), mkdir(), rmdir()를 비롯한 다른 화일들과 등록부관련함수들을 제공한다. QFile클라스는 remove()와 exists()를 비롯한 정적편의함수들을 제공한다.

## 제2절. 자료기지관리

Qt의 SQL모듈은 SQL자료기지들을 호출하기 위한 가동환경 및 자료기지에 의존하지 않는 대면부와 자료기지들을 사용자대면부에 통합하기 위한 클라스들의 모임을 제공한다.

### 1. 련결과 질문

SQL질문을 실행하려면 우선 자료기지와의 련결을 확립해야 한다. 일반적으로 자료기지련결은 응용프로그람을 기동할 때 호출하는 개별적인 함수에서 설정된다. 례를 들면

bool createConnection() {

QSqlDatabase *db = QSqlDatabase::addDatabase("QOCI8");

db→setHostName("mozart.konkordia.edu");

db→setDatabaseName("musicdb");

db→setUserName("gbatstone");

db→setPassword("T17aV44");

if (!db→open()) {

db→lastError().showMessage();

return false;

}

return true;

}

우선 QSqlDatabase::addDatabase()를 호출하여 QSqlDatabase객체를 창조한다. addDatabase()의 인수는 Qt가 자료기지호출에 사용해야 할 자료기지구동프로그람을 지정한다. 이 경우에는 Oracle을 사용한다.

다음으로 자료기지주콤퓨터이름, 자료기지이름, 사용자이름, 그리고 암호를 설정하고 련결을 열려고 시도한다. open()이 실패하면 QSqlError::showMessage()을 리용하여 오유통보문을 표시한다.

일반적으로 main()에서 createConnection()를 호출할수 있다.

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

if (!createConnection())

return 1;

...

return app.exec();

}

일단 련결이 확립되면 QSqlQuery을 사용하여 기초하고있는 자료기지가 유지하는 SQL문을 실행할수 있다. 례를 들면 여기에 SELECT문의 실행방법이 있다.

QSqlQuery query;

query.exec("SELECT title, year FROM cd WHERE year >= 1998");

exec()호출후에 질문의 결과모임을 항행할수 있다.

while (query.next()) {

QString title = query.value(0).toString();

int year = query.value(1).toInt();

cerr << title.ascii() << ": " << year << endl;

}

next()를 한번 호출하여 QSqlQuery가 결과모임의 첫 레코드에 위치하게 한다. next()의 련이은 호출은 끝에 이를 때까지 매번 한 레코드씩 레코드지적자를 전진시킨다. 끝점에서 next()는 false를 돌려준다. 결과모임이 비였으면 next()의 첫 호출은 false를 돌려준다.

value()함수는 마당값을 QVariant로서 돌려준다. 마당들에는 SELECT문에서 주어지는 순서로 0으로부터 번호가 붙는다. QVariant클라스는 int와 QString을 비롯한 수많은 C++와 Qt형들을 제공한다. 자료기지에 보관할수 있는 각이한 자료형들은 대응하는 C++ 및 Qt형들로 변환되고 QVariant들에 보관된다. 례를 들면 VARCHAR는 QString으로, DATETIME은 QDateTime으로 표시된다.

QSqlQuery는 결과모임을 항행하기 위한 다른 함수 즉 first(), last(), prev(), seek(), at()를 제공한다. 이러한 함수들은 편리하지만 일부 자료기지들에서 기억기가 모자란다. 큰 자료모임에 조작할 때 간단한 최적화를 위하여 exec()를 호출하기 전에 QSqlQuery:: setForwardOnly(true)를 호출할수 있으며 오직 결과모임을 항행할 때만 next()를 사용한다.

초기에 exec()의 인수로서 SQL질문을 지정하였으나 곧 실행하는 구성자에 SQL질문을 직접 넘길수 있다.

QSqlQuery query("SELECT title, year FROM cd WHERE year >= 1998");

여기에 오유를 검사하고 문제가 발생하는 경우에 QMessageBox를 펼치는 방법이 있다.

if (!query.isActive())

query.lastError().showMessage();

INSERT는 SELECT처럼 대체로 실행하기 쉽다.

QSqlQuery query("INSERT INTO cd (id, artistid, title, year) "

"VALUES (203, 102, 'Living in America', 2002)");

그다음에 QSqlQuery::numRowsAffected()는 SQL문의 영향을 받은 행수(혹은 자료기지가 그 정보를 제공할수 없으면 –1)를 돌려준다.

많은 레코드를 삽입해야 하거나 값들을 문자렬로 변환하지 않으려면(그리고 값들을 정확히 확장하려면) prepare()를 사용하여 대리기호를 포함하는 질문을 지정한 다음 삽입하려는 값들을 속박할수 있다. Qt는 모든 자료기지에서 Oracle형식과 ODBC형식의 대리기호문법을 유지한다. 이때 그 문법이 유효하면 그대로 리용하고 그렇지 않으면 모의한다. 여기에 이름있는 대리기호를 가지는 Oracle형식문법을 사용하는 실례가 있다.

QSqlQuery query(db);

query.prepare("INSERT INTO cd (id, artistid, title, year) " "VALUES (:id, :artistid,:title, :year)");

query.bindValue(":id", 203);

query.bindValue(":artistid", 102);

query.bindValue(":title", QString("Living in America"));

query.bindValue(":year", 2002);

query.exec();

여기에 ODBC형식의 위치대리기호를 리용하는 실례가 있다.

QSqlQuery query(db);

query.prepare("INSERT INTO cd (id, artistid, title, year) VALUES (?, ?, ?, ?)");

query.addBindValue(203); query.addBindValue(102);

query.addBindValue(QString("Living in America"));

query.addBindValue(2002);

query.exec();

prepare()호출후에 bindValue()나 addBindValue()를 호출하여 새 값들을 속박한 다음 다시 exec()를 호출하여 새 값들로 질문을 실행할수 있다.

대리기호는 흔히 두값자료 혹은 비 ASCII 혹은 비 Latin-1문자들을 포함하는 문자렬을 지정하는데 쓰인다. 이러한 배경하에서 Qt는 유니코드를 유지하는 자료기지들에서 유니코드를 사용하고 그렇지 않은것들에 대해서는 문자렬을 적당한 부호화로 명백히 변환한다.

Qt는 사용가능한 자료기지들에 대하여 SQL일괄처리를 유지한다. 일괄처리를 시작하려면 자료기지련결을 표시하는 QSqlDatabase객체에 대하여 transaction()을 호출한다. 일괄처리를 완료하려면 commit() 혹은 rollback()를 호출한다. 례를 들면 여기에 일괄처리내에서 외부열쇠를 찾고 INSERT문을 실행하는 방법이 있다.

QSqlDatabase::database()→transaction();

QSqlQuery query;

query.exec("SELECT id FROM artist WHERE name = 'Gluecifer'");

if (query.next()) {

int artistId = query.value(0).toInt();

query.exec("INSERT INTO cd (id, artistid, title, year) "

"VALUES (201, " + QString::number(artistId)+ ", 'Riding the Tiger', 1997)");

}

QSqlDatabase::database()→commit();

QSqlDatabase::database()함수는 createConnection()에서 생성한 QSqlDatabase객체의 지적자를 돌려준다. 일괄처리를 기동할수 없으면 QSqlDatabase::transaction()은 false를 돌려준다.

일부 자료기지들은 일괄처리를 유지하지 않는다. 그러한 경우에 transaction(), commit(), rollback()함수들은 아무것도 수행하지 않는다. 자료기지와 련결된 QSqlDriver에 대하여 hasFeature()를 리용하여 자료기지가 일괄처리를 유지하는가 시험할수 있다.

QSqlDriver*driver = QSqlDatabase::database()→driver();

if (driver→hasFeature(QSqlDriver::Transactions)) …

지금까지의 실례들에서는 응용프로그람이 단일한 자료기지련결을 리용하고있다고 가정하였다. 다중련결을 사용하려고 한다면 addDatabase()에 둘째 인수로서 이름을 넘길수 있다. 례를 들면

QSqlDatabase *db = QSqlDatabase::addDatabase("QPSQL7", "OTHER");

db→setHostName("saturn.mcmanamy.edu");

db→setDatabaseName("starsdb");

db→setUserName("gilbert");

db→setPassword("ixtapa6");

그다음 이름을 넘기여 QSqlDatabase객체의 지적자를 얻을수 있다.

QSqlDatabase::database():

QSqlDatabase *db = QSqlDatabase::database("OTHER");

다른 련결을 리용하여 질문을 실행하려면 QSqlDatabase객체를 QSqlQuery구성자에 넘겨야 한다.

QSqlQuery query(db);

query.exec("SELECT id FROM artist WHERE name = 'Mando Diao'");

매개의 련결이 오직 하나의 능동일괄처리만 처리할수 있으므로 다중련결은 한번에 하나이상의 일괄처리를 수행하려고 할 때 사용할수 있다. 다중자료기지련결을 사용한다면 여전히 하나의 이름없는 련결을 가질수 있으며 QSqlQuery은 아무것도 지정되지 않으면 그 련결을 사용한다.

QSqlQuery외에도 Qt는 고급한 클라스로서 QSqlCursor클라스를 제공한다. 이 클라스는 QSqlQuery를 계승하고 편의함수들을 확장하여 가장 일반적인 SQL조작 SELECT, INSERT, UPDATE, DELETE를 수행하는 본래의 SQL을 입력하는것을 피할수 있다. 또한 QSqlCursor는 QDataTable을 자료기지에 속박하는 클라스이다.

여기에 QSqlCursor을 리용하여 SELECT를 처리하는 실례가 있다.

QSqlCursor cursor("cd");

cursor.select("year >= 1998");

등가한 QSqlQuery은 다음과 같다.

QSqlQuery query("SELECT id, artistid, title, year FROM cd " "WHERE year>=1998");

결과모임의 항행은 QSqlQuery에서와 같은데 마당번호대신에 마당이름들을 value()에 넘길수 있다.

while (cursor.next()) {

QString title = cursor.value("title").toString();

int year = cursor.value("year").toInt();

cerr << title.ascii() << ": " << year << endl;

}

표에 레코드를 삽입하기 위하여 우선 newQSqlRecord의 지적자를 돌려주는 primeInsert()를 호출하여야 한다. 그다음 설정하려고 하는 QSqlRecord안의 매개 마당에 대하여 setValue()를 호출하고 insert()를 호출하여 QSqlRecord의 자료를 자료기지에 삽입한다. 례를 들면

QSqlCursor cursor("cd");

QSqlRecord *buffer = cursor.primeInsert();

buffer→setValue("id", 113);

buffer→setValue("artistid", 224);

buffer→setValue("title", "Shanghai My Heart");

buffer→setValue("year", 2003);

cursor.insert();

레코드를 갱신하려면 우선 수정하려는 레코드에 QSqlCursor를 배치해야 한다.(례를 들면 select()와 next()를 리용한다.) 그다음 primeUpdate()를 리용하여 레코드자료의 사본을 포함하는 QSqlRecord의 지적자를 얻는다. 그다음 setValue()를 리용하여 변경하려는 마당들을 설정하고 update()를 호출하여 이 변경을 자료기지에 써넣는다. 례를 들면

QSqlCursor cursor("cd");

cursor.select("id = 125");

if (cursor.next()) {

QSqlRecord *buffer = cursor.primeUpdate();

buffer→setValue("title", "Melody A.M.");

buffer→setValue("year", buffer→value("year").toInt() + 1);

cursor.update();

}

레코드의 삭제는 갱신과 비슷하지만 더 간단하다.

QSqlCursor cursor("cd");

cursor.select("id = 128");

if (cursor.next()) {

cursor.primeDelete();

cursor.del();

}

QSqlQuery과 QSqlCursor클라스들은 Qt와 SQL자료기지사이의 대면부를 제공한다.

### 2. 표형식의 창문에서 자료표시

QDataTable클라스는 열람과 편집기능을 가지는 자료기지인식 QTable창문부분품이다. 이 클라스는 QSqlCursor를 통하여 자료기지와 교제한다. 여기서는 QDataTable을 사용하는 2개의 대화창을 서술한다. 응용프로그람은 다음과 같이 정의된 3개의 표를 사용한다.

CREATE TABLE artist (id INTEGER PRIMARY KEY, name VARCHAR(40) NOT NULL, country VARCHAR(40));

CREATE TABLE cd (id INTEGER PRIMARY KEY, artistid INTEGER NOT NULL, title VARCHAR(40) NOT NULL, year INTEGER NOT NULL, FOREIGN KEY (artistid) REFERENCES artist);

CREATE TABLE track (id INTEGER PRIMARY KEY, cdid INTEGER NOT NULL,number INTEGER NOT NULL, title VARCHAR(40) NOT NULL, duration INTEGERNOT NULL, FOREIGN KEY (cdid) REFERENCES cd);

일부 자료기지는 외부열쇠를 제공하지 않는다. 이러한 자료기지에서는 FOREIGN KEY부들을 삭제해야 한다. 여전히 실례는 작업하지만 자료기지는 참고완전성을 가지지 않는다.

처음에 작성하는 클라스는 사용자가 기사목록을 편집하게 하는 대화칸이다. 사용자는 QDataTable의 문맥차림표를 리용하여 기사들을 삽입, 갱신, 혹은 삭제할수 있다. 이러한 변경은 사용자들이 Update를 찰칵할 때 자료기지에 적용된다.

accept()와 reject()처리부들은 QDialog로부터 재정의된다.

ArtistForm::ArtistForm(QWidget *parent, const char *name) : QDialog(parent, name) {

setCaption(tr("Update Artists"));

db = QSqlDatabase::database("ARTIST");

db→transaction();

QSqlCursor *artistCursor = new QSqlCursor("artist", true, db);

artistTable = new QDataTable(artistCursor, false, this);

artistTable→addColumn("name", tr("Name"));

artistTable→addColumn("country", tr("Country"));

artistTable→setAutoDelete(true); artistTable→setConfirmDelete(true);

artistTable→setSorting(true); artistTable→refresh();

updateButton = new QPushButton(tr("Update"), this);

updateButton→setDefault(true);

cancelButton = new QPushButton(tr("Cancel"), this);

connect(artistTable, SIGNAL(beforeDelete(QSqlRecord *)), this,

SLOT(beforeDeleteArtist(QSqlRecord *)));

connect(artistTable, SIGNAL(primeInsert(QSqlRecord *)), this,

SLOT(primeInsertArtist(QSqlRecord *)));

connect(artistTable, SIGNAL(beforeInsert(QSqlRecord *)), this,

SLOT(beforeInsertArtist(QSqlRecord *)));

connect(updateButton, SIGNAL(clicked()), this, SLOT(accept()));

connect(cancelButton, SIGNAL(clicked()), this, SLOT(reject()));

QHBoxLayout *buttonLayout = new QHBoxLayout;

buttonLayout→addStretch(1);

buttonLayout→addWidget(updateButton); buttonLayout→addWidget(cancelButton);

QVBoxLayout *mainLayout = new QVBoxLayout(this);

mainLayout→setMargin(11); mainLayout→setSpacing(6);

mainLayout→addWidget(artistTable); mainLayout→addLayout(buttonLayout);

}

ArtistForm구성자에서는 ARTIST자료기지련결을 리용하여 일괄처리를 시작한다. 그다음 자료기지의 기사표에 QSqlCursor를 창조하고 그것을 현시할 QDataTable를 창조한다.

QSqlCursor구성자의 둘째 인수는《자동거주》기발이다. true를 넘기여 QSqlCursor에 표의 매개 마당에 대한 정보를 적재하고 모든 마당들에 조작하게 한다.

QDataTable구성자의 둘째 인수도 역시 자동거주기발이다. true이면 QDataTable는 자동적으로 QSqlCursor의 결과모임안의 매개 마당용의 렬들을 창조한다. false를 넘기고 addColumn()를 호출하여 결과모임의 name과 country마당들에 대응하는 2개 렬을 제공한다.

setAutoDelete()를 호출하여 QSqlCursor의 소유자를 QDataTable에 넘기므로 그것을 자체로 삭제할 필요가 없다. setConfirmDelete()를 호출하여 QDataTable이 사용자에게 삭제를 확인하게 하는 통보창을 펼친다. setSorting(true)를 호출하여 사용자가 렬제목우에서 찰칵하여 렬에 따라서 표를 정렬하게 한다. 끝으로 refresh()를 호출하여 QDataTable에 자료기지의 자료를 채운다.

또한 Update와 Cancel단추를 창조한다.

QDataTable의 3개 신호를 3개의 비공개처리부들에 련결한다. Update단추를 accept()에, Cancel단추를 reject()에 련결한다.

끝으로 QPushButton들을 수평배치관리자에 넣고 QDataTable와 수평배치관리자를 수직배치관리자에 넣는다.

void ArtistForm::accept() { db→commit(); QDialog::accept(); }

사용자가 Update를 찰칵하면 일괄처리를 예약하고 기초클라스의 accept()함수를 호출한다.

void ArtistForm::reject() { db→rollback(); QDialog::reject(); }

사용자가 Cancel을 찰칵하면 일괄처리를 되돌리고 기초클라스의 reject()함수를 호출한다.

void ArtistForm::beforeDeleteArtist(QSqlRecord *buffer) {

QSqlQuery query(db);

query.exec("DELETE FROM track WHERE track.id IN (SELECT track.id FROM track, "

" cd WHERE track.cdid = cd.id AND cd.artistid = "

+ buffer→value("id").toString() + ")");

query.exec("DELETE FROM cd WHERE artistid = " + buffer→value("id").toString());

}

beforeDeleteArtist()처리부는 레코드가 삭제되기직전에 발생되는 QDataTable의 beforeDelete()신호에 련결된다. 여기서는 기사에 의하여 CD들로부터 모든 자리길들을 삭제할데 대한 질문과 기사에 의해 모든 CD들을 삭제할데 대한 질문을 실행함으로써 폭포식(종속적인) 삭제를 수행한다. 이러한 삭제는 관계완전성에 위험을 주지 않는다. 그것은 이러한 삭제가 형태의 구성자에서 시작되는 일괄처리의 상태에서 모두 수행되기때문이다.

또 다른 수법은 사용자가 cd표에 의해 참고되는 기사들을 삭제하지 않도록 하는것이다.

이것을 달성하려면 QDataTable::contextMenuEvent()를 재정의하여 삭제를 자체로 처리해야 한다. 자료기지가 관계완전성을 실시하도록 설정된 경우에 작업하는 초기의 수법은 단순히 삭제를 시도하고 자료기지에 그것을 맡기여 미연에 방지하는것이다.

void ArtistForm::primeInsertArtist(QSqlRecord *buffer){

buffer→setValue("country", "DPRK");

}

primeInsertArtist()처리부는 사용자가 새 레코드의 편집을 시작하기직전에 발생되는 QDataTable의 primeInsert()신호에 련결된다. 이 처리부를 리용하여 새 레코드의 country마당의 기정값을 우리 나라에서 사용하는 응용프로그람의 리상적인 기정값인 "DPRK"로 설정한다.

이것은 마당에 기정값을 설정하는 한가지 수법이다. 또 하나의 수법은 QSqlCursor의 파생클라스를 만들고 primeInsert()를 재정의하는것이다. 이 함수는 같은 응용프로그람에서 같은 QSqlCursor를 여러번 사용하고 일관한 동작을 담보하려고 하는 경우에 의의를 가진다. 셋째 수법은 CREATE TABLE문의 DEFAULT절을 사용하는 자료기지준위에서 수행하는것이다.

void ArtistForm::beforeInsertArtist(QSqlRecord *buffer){

buffer→setValue("id", generateId("artist", db));

}

beforeInsertArtist()처리부는 사용자가 새 레코드의 편집을 완료하고 그것을 보관하기 위하여 Enter건을 눌렀을 때 발생되는 QDataTable의 beforeInsert()신호에 련결된다. id마당의 값을 생성된 값으로 설정한다. generateId()라는 함수에 기초하여 유일한 주열쇠(primary key)를 생성한다.

generateId()를 여러번 생성해야 하므로 머리부화일에서 이 함수를 inline으로 정의하고 그것이 요구될 때마다 포함한다. 여기에 그것을 실현하는 빠른(비효과적인) 수법이 있다.

inline int generateId(const QString &table, QSqlDatabase *db) {

QSqlQuery query(db);

query.exec("SELECT max(id) FROM " + table);

query.next();

return query.value(0).toInt() + 1;

}

generateId()함수는 대응하는 INSERT문과 같은 일괄처리의 경우에 실행된다면 정확한 동작을 담보할수 있다.

일부 자료기지는 자동생성되는 마당들을 유지한다. 이 마당들과 관련하여 단지 자료기지에 id마당들을 자동생성한다고 알리고 QSqlCursor에 대하여 setGenerated("id", false)를 호출하여 id마당의 값을 생성하지 않는다고 말한다.

이제 QDataTable를 사용하는 다른 대화창을 론의한다. 이 대화창에서는 주-세부보기를 실현한다. 주(기본)보기는 CD들의 목록이다. 세부보기는 현재 CD의 자리길목록이다. 이 대화창은 CD Collection응용프로그람의 기본창문이다.

### 3. 자료인식창의 창조

Qt는 자료기지와 대면형식창들사이의 교제를 갱신하는 수법을 제공한다. 각 기본창문부분품에 대하여 제각기 자료기지허용판을 만드는것이 아니라 Qt는 자료기지마당들을 창문부분품들과 련결하는데 QSqlForm와 QSqlPropertyMap를 사용하여 임의의 창문부분품이 자료를 인식하게 만들수 있다. 기본창문부분품이나 사용자정의창문부분품은 이러한 클라스들을 사용하여 자료를 인식하게 만들수 있다.

QSqlForm은 형태들을 창조하여 자료기지안의 개별적인 레코드들을 간단히 열람하거나 편집하게 하는 QObject의 파생클라스이다. 일반적인 사용법은 다음과 같다.

① 레코드의 마당들에 대응하는 편집기창문부분품들(QLineEdits, QComboBoxes, QSpinBoxes 등)을 창조한다.

② QSqlCursor을 창조하고 그것을 편집하려는 레코드로 옮긴다.

③ QSqlForm객체를 창조한다.

④ QSqlForm에게 어느 편집기창문부분품이 어느 자료기지마당에 결합되는가를 알린다.

⑤ QSqlForm::readFields()함수를 호출하여 현재 레코드로부터 편집기창문부분품들에 자료를 옮긴다.

⑥ 대화창을 표시한다.

⑦ QSqlForm::writeFields()함수를 호출하여 갱신된 값을 자료기지에 복사한다.

이것을 설명하기 위하여 CdForm대화창의 코드를 론의한다. 이 대화창은 사용자가 CD레코드를 창조하거나 편집하게 한다. 사용자는 CD의 제목, 기사, 제작년도와 매개 자리길의 제목과 연주시간을 지정할수 있다.

2개의 구성자를 선언한다. 즉 하나는 새 CD를 자료기지에 삽입하기 위한 구성자이고 다른 하나는 현존 CD를 갱신하기 위한 구성자이다. accept()와 reject()처리부들은 QDialog로부터 재정의된다.

CdForm::CdForm(QWidget *parent, const char *name) : QDialog(parent, name) {

setCaption(tr("Add a CD"));

cdId = -1;

init();

}

첫 구성자는 대화창의 제목을 "Add a CD"로 설정하고 비공개 init()함수를 호출하여 남은 일을 수행한다.

CdForm::CdForm(int id, QWidget *parent, const char *name) : QDialog(parent, name) {

setCaption(tr("Edit a CD"));

cdId = id;

init();

}

둘째 구성자는 제목을 "Edit a CD"로 설정하고 역시 init()를 호출한다.

void CdForm::init() {

db = QSqlDatabase::database("CD");

db→transaction();

if (cdId == -1)

createNewRecord();

titleLabel = new QLabel(tr("&Title:"), this);

artistLabel = new QLabel(tr("&Artist:"), this);

yearLabel = new QLabel(tr("&Year:"), this);

titleLineEdit = new QLineEdit(this);

yearSpinBox = new QSpinBox(this);

yearSpinBox→setRange(1900, 2100);

yearSpinBox→setValue(QDate::currentDate().year());

artistComboBox = new ArtistComboBox(db, this);

artistButton = new QPushButton(tr("Add &New..."), this);

...

cancelButton = new QPushButton(tr("Cancel"), this);

trackCursor = new QSqlCursor("track", true, db);

trackTable = new QDataTable(trackCursor, false, this);

trackTable→setFilter("cdid = " + QString::number(cdId));

trackTable→setSort(trackCursor→index("number"));

trackTable→addColumn("title", tr("Track"));

trackTable→addColumn("duration", tr("Duration"));

trackTable→refresh();

cdCursor = new QSqlCursor("cd", true, db);

cdCursor→select("id = " + QString::number(cdId));

cdCursor→next();

QSqlPropertyMap *propertyMap = new QSqlPropertyMap;

propertyMap→insert("ArtistComboBox", "artistId");

sqlForm = new QSqlForm(this);

sqlForm→installPropertyMap(propertyMap);

sqlForm→setRecord(cdCursor→primeUpdate());

sqlForm→insert(titleLineEdit, "title");

sqlForm→insert(artistComboBox, "artistid");

sqlForm→insert(yearSpinBox, "year");

sqlForm→readFields();

connect(artistButton, SIGNAL(clicked()), this, SLOT(addNewArtist()));

connect(moveUpButton, SIGNAL(clicked()), this, SLOT(moveTrackUp()));

connect(moveDownButton, SIGNAL(clicked()), this, SLOT(moveTrackDown()));

connect(updateButton, SIGNAL(clicked()), this, SLOT(accept()));

connect(cancelButton, SIGNAL(clicked()), this, SLOT(reject()));

connect(trackTable, SIGNAL(beforeInsert(QSqlRecord *)), this,

SLOT(beforeInsertTrack(QSqlRecord *)));

...

}

init()에서는 CD자료기지련결을 리용하여 일괄처리를 시작한다. CdForm과 ArtistForm에서는 다른 련결들을 사용해야 한다. 그것은 두개 대면형식창을 동시에 열고 한 대면형식창이 다른 대면형식창에 의해 시작된 일괄처리를 되살리려고 하지 않기때문이다.

조작할 CD가 없다면 비공개함수 createNewRecord()를 호출하여 자료기지에 빈CD를 삽입한다. 이것은 자리길들의 QDataTable에서 CD ID를 외부열쇠로 사용하게 한다. 사용자들이 Cancel을 찰칵하면 일괄처리를 되돌리고 빈 레코드는 표시되지 않는다.

이 대화창에서는 ArtistForm에서와는 다른 자료기지련결을 사용한다. 그것은 련결당 오직 하나의 능동일괄처리를 가질수 있으므로 두 일괄처리를 요구하는 경우에 례를 들면 사용자가 Add New단추를 찰칵하여 ArtistForm을 펼치는 경우에 완료할수 있기때문이다.

사용자대면부를 형성하는 표식자들과 행편집칸, 스핀칸, 복합칸단추들을 창조한다. 복합칸은 후에 설명하는 ArtistComboBox형이다.

사용자가 현재 CD의 자리길들을 열람 및 편집하게 하는 QDataTable을 설정한다.

QSqlForm과 련관된 QSqlCursor를 설정하고 그것이 현재 ID를 가지는 레코드를 지적하게 한다.

QSqlPropertyMap를 창조한다. QSqlPropertyMap클라스는 QSqlForm에게 어느 Qt속성이 어떤형의 편집기창문부분품의 값을 보관하는가를 말해준다. 기정으로 이미 QSqlForm은 QLineEdit가 값을 text속성에 보관하고 QSpinBox는 값을 value속성에 보관한다는것을 알고있다. 그러나 ArtistComboBox와 같은 사용자정의창문부분품들에 대해서는 전혀 모른다. 속성매프에 쌍("ArtistComboBox", "artistId")을 삽입하고 QSqlForm에 대하여 installPropertyMap()을 호출함으로써 QSqlForm에 ArtistComboBox형의 창문부분품들에서 artistId속성을 사용한다는것을 알린다.

또한 QSqlForm객체는 조작할 완충기를 요구하며 완충기는 QSqlCursor에 대하여 primeUpdate()를 호출하여 얻어지며 어느 편집기창문부분품이 어느 자료기지마당에 대응하는가를 알아야 한다. 끝으로 readFields()를 호출하여 자료기지로부터 편집기창문부분품들에 자료를 읽어들인다.

단추들의 clicked()신호들과 QDataTable의 beforeInsert()신호를 다음에 서술하는 비공개처리부들에 련결한다.

void CdForm::accept(){

sqlForm→writeFields();

cdCursor→update();

db→commit();

QDialog::accept();

}

사용자가 Update를 찰칵하면 자료를 QSqlCursor의 편집완충기에 써넣고 update()를 호출하여 자료기지에 대하여 UPDATE를 수행하고 commit()를 호출하여 실제로 레코드를 자료기지에 써넣으며 기초클라스의 accept()실현을 호출하여 대면형식창을 닫는다.

void CdForm::reject() { db→rollback(); QDialog::reject(); }

사용자가 Cancel단추를 찰칵하면 되돌아와서 자료기지를 변경하지 않은대로 놔두고 대면형식창을 닫는다.

void CdForm::addNewArtist(){

ArtistForm form(this);

if (form.exec()) {

artistComboBox→refresh();

updateButton→setEnabled(artistComboBox→count() > 0);

}

}

사용자가 Add New단추를 찰칵하면 이행금지 ArtistForm대화창이 펼쳐진다. 대화창은 사용자가 새 기사들을 추가하게 하고 또한 현존 기사들을 편집 및 삭제하게 한다. 사용자가 Update단추를 찰칵하면 ArtistComboBox::refresh()를 호출하여 그 기사목록이 갱신되도록 한다.

새 CD를 기사이름이 없이 창조하지 않게 하려고 하므로 기사가 있는가 없는가에 따라 Update단추를 허용하거나 금지한다.

void CdForm::beforeInsertTrack(QSqlRecord *buffer){

buffer→setValue("id", generateId("track", db));

buffer→setValue("number", trackCursor→size() + 1);

buffer→setValue("cdid", cdId);

}

beforeInsertTrack()처리부는 QDataTable의beforeInsert()신호에 련결된다. 레코드의id, 번호, 그리고 cdid마당들을 설정한다.

void CdForm::beforeDeleteTrack(QSqlRecord *buffer){

QSqlQuery query(db);

query.exec("UPDATE track SET number = number -1 WHERE track.number > "

+ buffer→value("number").toString());

}

beforeDeleteTrack()처리부는 QDataTable의beforeDelete()신호에 련결된다. 삭제한 자리길보다 큰 수를 가지는 모든 자리길들의 번호를 다시 지정하여 자리길번호들이 련결되도록 한다. 례를 들면 CD에 6개의 자리길이 있고 사용자가 자리길 4를 삭제하면 자리길 5는 자리길 4로 되고 자리길 6은 자리길 5로 된다.

아직 설명하지 않은 4개의 함수 moveTrackUp(), moveTrackDown(), swapTracks(), createNewRecord()가 있다. 이 함수들은 응용프로그람을 사용할수 있게 하는데 필요하지만 그 실현은 어떤 새로운 기술도 보여주지 않으므로 여기서 론의하지 않는다.

## 제3절. 망통신

Qt는 FTP 및 HTTP와 작업하기 위한 QFtp와 QHttp클라스를 제공한다. 이 통신규약들은 화일들을 내리적재 및 올리적재하는데 사용하기 쉬우며 HTTP의 경우에 웨브봉사기들에 요구를 보내고 결과를 얻는데 사용하기 편리하다.

Qt의 QFtp와 QHttp클라스들은 TCP소케트를 제공하는 저수준QSocket클라스에 구축된다.

TCP는 망마디들사이에 전송되는 자료흐름에 의하여 조작된다. 또한 QSocket는 가동환경에 고유한 망API와 가까운 QSocketDevice에 실현된다. QSocketDevice클라스는 TCP와 UDP를 둘다 유지한다.

### 1. QFtp의 리용

QFtp클라스는 Qt에서 FTP통신규약의 의뢰기측을 실현한다. 이 클라스는 get(), put(), remove(), mkdir()를 비롯한 가장 일반적인 FTP조작들을 수행하기 위한 여러가지 함수들을 제공하며 임의의 FTP지령들을 실행하는 수단을 제공한다.

QFtp클라스는 비동기적으로 작업한다. get()나 put()와 같은 함수를 호출할 때 곧 되돌아오며 Qt의 사건순환고리로 조종이 넘어올 때 자료전송이 발생한다. 이것은 FTP지령들을 실행하는동안 사용자대면부에 응답성이 유지된다는것을 담보한다.

get()에 의해 하나의 화일을 얻는 방법을 보여주는 실례로 시작한다. 실례는 응용프로그람의 MainWindow클라스가 FTP싸이트로부터 값목록을 얻는데 필요하다고 가정한다.

이 클라스는 값목록화일을 얻는 공개함수 getPriceList()와 화일전송이 완료될 때 호출되는 비공개처리부 ftpDone(bool)을 가진다. 또한 이 클라스는 2개의 비공개변수를 가진다. ftp변수는 QFtp형으로서 FTP봉사기에로의 련결을 밀봉하고 file변수는 내리적재한 화일을 디스크에 써넣는데 쓰인다.

MainWindow::MainWindow(QWidget *parent, const char *name) : QMainWindow(parent, name) {

...

connect(&ftp, SIGNAL(done(bool)), this, SLOT(ftpDone(bool)));

}

구성자에서는 QFtp객체의 done(bool)신호를 ftpDone(bool)비공개처리부에 련결한다. QFtp는 모든 요구에 대한 처리가 끝났을 때 done(bool)신호를 발생한다. bool파라메터는 오유가 있는가 없는가를 가리킨다.

void MainWindow::getPriceList() {

file.setName("price-list.csv");

if (!file.open(IO_WriteOnly)) {QMessageBox::warning(this, tr("Sales Pro"), tr("Cannot write file %1\n%2."). arg(file.name()) .arg(file.errorString()));

return;

}

ftp.connectToHost("ftp.trolltech.com");

ftp.login(); ftp.cd("/topsecret/csv");

ftp.get("price-list.csv", &file);

ftp.close();

}

getPriceList()함수는 ftp://ftp.trolltech.com/topsecret/csv/price-list.csv화일을 내리적재하여 현재 등록부의 price-list.csv로서 보관한다.

우선 써넣으려는 QFile을 연다. 그다음 QFtp객체를 리용하여 5개의 FTP지령을 차례로 실행한다. get()의 둘째 인수는 출력장치를 지정한다.

FTP지령들은 Qt의 사건순환고리에서 대기하고있다가 실행된다. 지령의 완료는 구성자에서 ftpDone(bool)에 련결된 QFtp의 done(bool)신호에 의하여 알려진다.

void MainWindow::ftpDone(bool error) {

if (error)

QMessageBox::warning(this, tr("Sales Pro"),

tr("Error while retrieving file with FTP: %1.").arg(ftp.errorString()));

file.close();

}

일단 FTP지령들이 실행되면 화일을 닫는다. 오유가 발생하면 그것을 QMessageBox에 현시한다.

QFtp는 다음의 조작 즉 connectToHost(), login(), close(), list(), cd(), get(), put(), remove(), mkdir(), rmdir() 그리고 rename()를 제공한다. 이 함수들은 모두 FTP지령을 발생하고 지령을 식별하는 ID번호를 돌려준다. 임의의 FTP지령들은 rawCommand()에 의해 실행될수 있다. 례를 들면 여기에 SITE CHMOD지령을 실행하는 방법이 있다.

ftp.rawCommand("SITE CHMOD 755 fortune");

QFtp는 지령실행을 시작할 때 commandStarted(int)신호를 발생하고 지령이 끝날 때 commandFinished(int, bool)신호를 발생한다. int파라메터는 지령을 식별하는 ID번호이다. 개별적인 지령들의 수명에 관심이 있으면 지령들을 실행할 때 ID번호들을 보관할수 있다. ID번호를 리용하여 사용자에게 지령에 대한 세부적인 처리를 제공할수 있다.

반결합을 제공하는 다른 하나의 수법은 QFtp의 stateChanged()신호에 련결하는것이다.

대부분의 응용프로그람들에서는 오직 지령들의 전체 렬에 관심을 가진다. 그때 지령기다림렬이 빌 때마다 발생되는 done(bool)신호를 단순히 련결할수 있다.

오유가 발생하면 QFtp는 자동적으로 지령기다림렬을 지운다. 이것은 련결이나 로그인이 실패하면 기다림렬의 뒤를 따르는 지령들은 절대로 실행되지 않는다는것을 의미한다. 그러나 오유발생후에 같은 QFtp객체를 리용하여 새 지령들을 실행한다면 이 지령들은 아무것도 발생하지 않은것처럼 기다렸다가 실행된다.

Downloader클라스는 FTP등록부에 배치되는 모든 화일들을 내리적재한다. 등록부는 클라스의 구성자에 넘긴 QUrl로서 지정된다. QUrl클라스는 화일이름, 경로, 통신규약 및 포구와 같은 URL의 각 부분들을 꺼내기 위한 고급한 대면부를 제공하는 Qt클라스이다.

Downloader::Downloader(const QUrl &url) {

if (url.protocol() != "ftp") {

QMessageBox::warning(0, tr("Downloader"), tr("Protocol must be 'ftp'."));

emit finished();

return;

}

int port = 21;

if (url.hasPort())

port = url.port();

connect(&ftp, SIGNAL(done(bool)), this, SLOT(ftpDone(bool)));

connect(&ftp, SIGNAL(listInfo(const QUrlInfo &)), this, SLOT(listInfo(const QUrlInfo &)));

ftp.connectToHost(url.host(), port);

ftp.login(url.user(), url.password()); ftp.cd(url.path());

ftp.list();

}

구성자에서는 우선 URL이 "ftp:"로 시작하는가 검사한다. 그다음 포구번호를 꺼낸다. 포구가 지정되지 않으면 FTP의 기정포구인 포구 21을 사용한다.

다음으로 2개의 신호–처리부련결을 확립하고 4개의 FTP지령들을 실행한다. 마지막 FTP지령 list()는 등록부안의 매개 화일이름을 얻으며 얻어지는 매개 이름에 대하여 listInfo(const QUrlInfo &)신호를 발생한다. 이 신호는 주어진 URL과 련관된 화일을 내리적재하는 listInfo()라고 부르는 처리부에 련결된다.

void Downloader::listInfo(const QUrlInfo &urlInfo) {

if (urlInfo.isFile() && urlInfo.isReadable()) {

QFile *file = new QFile(urlInfo.name());

if (!file→open(IO_WriteOnly)) {

QMessageBox::warning(0, tr("Downloader"), tr("Error: Cannot open file %1:\n%2.").arg(file→name()) .arg(file→errorString()));

emit finished();

return;

}

ftp.get(urlInfo.name(), file);

openedFiles.push_back(file);

}

}

listInfo()처리부의 QUrlInfo파라메터는 원격화일에 대한 자세한 정보를 제공한다. 화일이 표준화일(등록부아님.)이고 읽기가능하다면 get()를 호출하여 그것을 내리적재한다. 내리적재에 사용된 QFile객체는 new에 의하여 할당되고 그 지적자는 openedFiles벡토르에 보관된다.

void Downloader::ftpDone(bool error){

if (error)

QMessageBox::warning(0, tr("Downloader"), tr("Error: %1.") .arg(ftp.errorString()));

for (int i = 0;i < (int)openedFiles.size();++i)

delete openedFiles[i];

emit finished();

}

ftpDone()처리부는 FTP지령들이 모두 완료하였을 때 혹은 오유가 발생하면 호출된다.

QFile객체들을 삭제하여 기억루실을 방지하고 또한 매개 화일을 닫는다.(QFile해체자는 화일이 열려있으면 자동적으로 닫는다.)

### 2. QHttp의 리용

QHttp클라스는 Qt에서 HTTP통신규약의 의뢰기측을 실현한다. 이 클라스는 get()와 post()를 비롯한 가장 일반적인 HTTP조작들을 수행하는 각종 함수들을 제공하고 임의의 HTTP요구를 보내는 수단을 제공한다.

QHttp클라스는 비동기적으로 작업한다. get()나 post()와 같은 함수를 호출할 때 함수는 곧 되돌아오고 후에 조종이 Qt의 사건순환고리에 돌아올 때 자료전송이 발생한다. 이것은 HTTP요구를 처리하는동안에 응용프로그람의 사용자대면부가 응답성을 유지하도록 한다.

Qt응용프로그람의 MainWindow클라스에서 Trolltech의 웨브싸이트로부터 HTML화일을 내리적재하는 방법을 보여준다. 머리부화일에는 하나의 비공개처리부(httpDone(bool))와 비공개변수들(QHttp형의 http와 QFile형의 file)이 있다.

MainWindow::MainWindow(QWidget *parent, const char *name) : QMainWindow(parent, name){

...

connect(&http, SIGNAL(done(bool)), this, SLOT(httpDone(bool)));

}

구성자에서는 QHttp객체의 done(bool)신호를 MainWindow의 httpDone(bool)처리부에 련결한다.

void MainWindow::getFile() {

file.setName("aboutQt.html");

if (!file.open(IO_WriteOnly)) {

QMessageBox::warning(this, tr("HTTP Get"), tr("Cannot write file %1\n%2.")

.arg(file.name()) .arg(file.errorString()));

return;

}

http.setHost("doc.trolltech.com"); http.get("/3.2/aboutQt.html", &file);

http.closeConnection();

}

getFile()함수는 http://doc.trolltech.com/3.2/aboutQt.html화일을 내리적재하여 현재등록부에 aboutQt.html로서 보관한다.

QFile을 써넣기용으로 열고 QHttp객체를 리용하여 3개의 HTTP요구들의 렬을 실행한다.

get()의 둘째 인수는 출력장치를 지정한다.

HTTP요구들은 Qt의 사건순환고리에서 기다렸다가 실행된다. 지령의 완료는 구성자에서 httpDone(bool)에 련결된 QHttp의 done(bool)신호에 의해 지적된다.

void MainWindow::httpDone(bool error) {

if (error)

QMessageBox::warning(this, tr("HTTP Get"),

tr("Error while fetching file with HTTP: %1.").arg(http.errorString()));

file.close();

}

일단 HTTP요구들이 완료되면 화일을 닫는다. 오유가 발생하였다면 QMessageBox에 오유통보문을 현시한다.

QHttp는 다음의 조작 즉 setHost(), get(), post(), head()를 제공한다. 례를 들면 여기에 post()를 리용하여 "name = value"쌍들의 목록을 CGI스크립트에 보내는 방법이 있다.

http.setHost("www.example.com");

http.post("/cgi/somescript.py", QCString("x=200&y=320"), &file);

많은 조종들에서 임의의 HTTP머리부와 자료를 받아들이는 request()함수를 사용할수 있다.

례를 들면

QHttpRequestHeader header("POST", "/search.html");

header.setValue("Host", "www.trolltech.com");

header.setContentType("application/x-www-form-urlencoded");

http.setHost("www.trolltech.com");

http.request(header, QCString("Qt-interest=on&search=opengl"));

QHttp는 요구의 실행을 시작할 때 requestStarted(int)신호를 발생하고 요구가 완료되였을 때 requestFinished(int, bool)신호를 발생한다. int파라메터는 요구를 식별하는 ID번호이다. 개별적인 요구들의 수명에 관심이 있다면 요구들을 실행할 때 ID번호들을 보관할수 있다. ID번호를 리용하여 사용자에게 요구에 대한 세부적인 조종을 제공할수 있다.

대부분의 응용프로그람들에서는 요구들의 전체렬이 성과적으로 끝났는가 아닌가를 알려고만 한다. 이것은 요구기다림렬이 비게 될 때 발생되는 done(bool)신호에 련결하여 간단히 달성한다.

오유가 발생하면 요구는 자동적으로 지워진다. 그러나 오유발생후에 같은 QHttp객체를 리용하여 새로운 요구를 실행한다면 이 요구들은 보통과 같이 기다렸다가 전송된다.

QFtp처럼 QHttp는 입출력장치를 지정할 대신에 사용할수 있는 readBlock()와 readAll()함수들은 물론 readyRead()신호를 제공한다. 또한 QProgressBar 혹은 QProgressDialog의 setProgress(int, int)처리부에 련결할수 있는 dataTransferProgress(int, int)신호를 제공한다.

### 3. QSocket를 리용한 TCP망프로그람작성

QSocket클라스는 TCP의뢰기와 봉사기들을 실현하는데 쓰일수 있다. TCP는 FTP와 HTTP를 비롯한 수많은 응용층Internet통신규약들의 기초를 이루는 전송층통신규약으로서 전용통신규약들에도 사용할수 있다.

TCP는 흐름지향통신규약이다. 응용프로그람들에서 자료는 크고 평탄한 화일보다도 긴 흐름으로 나타난다. TCP상에서 구축된 웃준위통신규약들은 일반적으로 행지향 혹은 블로크지향이다.

·행지향통신규약들은 자료를 행바꾸기로 구분한 본문행으로 전송한다.

·블로크지향통신규약들은 자료를 두값자료블로크들로 전송하다. 매개 블로크는 크기마당과 그뒤의 자료의 크기byte로 구성된다.

QSocket는 QIODevice를 계승하므로 QDataStream 혹은 QTextStream을 리용하여 읽고쓸수 있다. 망으로부터 자료를 읽어들일 때 화일로부터 읽어들일 때와 다른 한가지 중요한 차이는 >>연산자를 사용하기 전에 동료로부터 충분한 자료를 받았다는것을 확인해야 하는것이다. 여기서의 실패는 정의되지 않은 동작을 발생시킬수 있다.

의뢰기는 Trip Planner라고 부르고 사용자들이 다음번 렬차려행을 계획하게 한다. 봉사기는 TripServer라고 부르며 의뢰기에 려행정보를 제공한다. Trip Planner응용프로그람을 쓰는것으로 시작한다.

Trip Planner는 From마당, To마당, Date마당, Approximate Time마당 각각 하나씩과근사시간이 출발시간인가 도착시간인가를 선택하는 2개의 라지오단추들을 제공한다.

사용자가 Search를 찰칵할 때 응용프로그람은 요구를 봉사기에 보내고 봉사기는 사용자의 기준에 맞는 렬차려행들의 목록으로 응답한다.

목록은 Trip Planner창문의 QListView에 표시된다. 창문의 제일 아래에는 마지막조작의 상태를 보여주는 QLabel과 QProgressBar이 있다.

Trip Planner의 사용자대면부는 Qt Designer로 창조한다. 여기서 대응하는 .ui.h화일의 원천코드에 초점을 둔다. 다음의 4개 변수를 Qt Designer의 Members태브에서 선언한다.

QSocket socket;

QTimer connectionTimer;

QTimer progressBarTimer;

Q_UINT16 blockSize;

QSocket형의 socket변수는 TCP련결을 밀봉한다. connectionTimer변수는 오래 지속되는 련결시간을 요구하는데 쓰인다. progressBarTimer변수는 응용프로그람이 작업중에 있을 때 진척정형띠를 주기적으로 갱신하는데 쓰인다. 끝으로 blockSize변수는 봉사기로부터 받은 블로크들을 해석할 때 사용된다.

void TripPlanner::init() {

connect(&socket, SIGNAL(connected()), this, SLOT(sendRequest()));

connect(&socket, SIGNAL(connectionClosed()), this, SLOT(connectionClosedByServer()));

connect(&socket, SIGNAL(readyRead()), this, SLOT(updateListView()));

connect(&socket, SIGNAL(error(int)), this, SLOT(error(int)));

connect(&connectionTimer, SIGNAL(timeout()), this, SLOT(connectionTimeout()));

connect(&progressBarTimer, SIGNAL(timeout()), this, SLOT(advanceProgressBar()));

QDateTime dateTime = QDateTime::currentDateTime();

dateEdit→setDate(dateTime.date());

timeEdit→setTime(QTime(dateTime.time().hour(), 0));

}

init()에서는 QSocket의 connected(), connectionClosed(), readyRead(), error(int)신호들과 두개 시계들의 timeout()신호들을 자체의 처리부들에 련결한다. 또한 Date와 Approximate Time마당들에 현재 날자와 시간에 기초한 기정값들을 채워넣는다.

void TripPlanner::advanceProgressBar() {

progressBar→setProgress(progressBar→progress() + 2);

}

advanceProgressBar()처리부는 progressBarTimer의 timeout()신호에 련결된다.

진척정형띠를 2단위 전진시킨다. Qt Designer에서 진척정형띠의 totalSteps속성을 띠가 작업중 지시기로서 동작해야 한다는것을 의미하는 특수값인 0으로 설정한다.

void TripPlanner::connectToServer() {

listView→clear();

socket.connectToHost("tripserver.zugbahn.de", 6178);

searchButton→setEnabled(false); stopButton→setEnabled(true);

statusLabel→setText(tr("Connecting to server…"));

connectionTimer.start(30 * 1000, true);

progressBarTimer.start(200, false);

blockSize = 0;

}

connectToServer()처리부는 사용자가 탐색을 시작하기 위하여 Search를 찰칵할 때 실행된다.

QSocket객체에 대하여 connectToHost()를 호출하여 봉사기에 련결한다. 이때 가상주콤퓨터 tripserver.zugbahn.de를 포구 6178에서 호출할수 있다고 가정한다.(자기의 콤퓨터에서 실례를 실행하려고 한다면 주콤퓨터이름을 국부주콤퓨터로 고친다.)

connectToHost()호출은 비동기적이고 곧 되돌아온다. 일반적으로 련결은 후에 수립된다. QSocket객체는 련결이 이루어지고 실행될 때 connected()신호를 발생하고 련결이 실패하면 error(int)(오유코드와 함께)를 발생한다.

다음으로 사용자대면부를 갱신하고 2개의 시계를 기동한다. 첫째 시계 connection Timer는 련결이 30s동안 이루어지지 않았을 때 절환되는 단일발사시계이다. 둘째 시계 progressBarTimer는 매번 200㎳간격으로 사건을 발생하여 응용프로그람의 진척정형띠를 갱신하며 응용프로그람이 작업하고있다는 시각적인 암시를 사용자에게 준다.

끝으로 blockSize변수를 0으로 설정한다. blockSize변수는 봉사기로부터 받은 블로크의 길이를 보관한다. 다음에는 블로크크기를 아직 모른다는것을 의미하는 값 0을 사용하기로 선택하였다.

void TripPlanner::sendRequest() {

QByteArray block;

QDataStream out(block, IO_WriteOnly);

out.setVersion(5);

out << (Q_UINT16)0 << (Q_UINT8) 'S'

<< fromComboBox→currentText()

<< toComboBox→currentText() << dateEdit→date()

<< timeEdit→time();

if (departureRadioButton→isOn())

out << (Q_UINT8) 'D';

else

out << (Q_UINT8) 'A';

out.device()→at(0);

out << (Q_UINT16) (block.size() -sizeof(Q_UINT16));

socket.writeBlock(block.data(), block.size());

statusLabel→setText(tr("Sending request…"));

}

sendRequest()처리부는 련결이 확립되였다는것을 가리키는 connected()신호를 QSocket객체가 발생할 때 실행된다. 그 처리부의 과제는 사용자가 입력한 모든 정보를 가지는 요구를 봉사기에 생성하는것이다.

우선 날자를 블로크라고 부르는 QByteArray에 써넣는다. 블로크안에 자료를 모두 넣은 다음에야 처음에 전송해야 할 블로크의 크기를 알수 있으므로 QSocket에 직접 자료를 써넣을수 있다.

초기에 블로크크기로서 0을 써넣고 다음에 자료의 나머지가 뒤에 온다. 그다음 입출력장치(배경에서 QDataStream에 의해 창조된 QBuffer)에 대하여 at(0)을 호출하여 byte배렬의 선두로 이동하고 블로크자료의 크기와 함께 0을 다시 써넣는다. 크기는 블로크크기에 sizeof(Q_UINT16)(즉 2)를 덜어서 byte량에서 크기마당을 제외한다. 그후에 QSocket에 대하여 writeBlock()를 호출하여 봉사기에 블로크를 보낸다.

void TripPlanner::updateListView() {

connectionTimer.start(30 * 1000, true);

QDataStream in(&socket);

in.setVersion(5);

for (;;) {

if (blockSize == 0) {

if (socket.bytesAvailable() < sizeof(Q_UINT16))

break;

in >> blockSize;

}

if (blockSize == 0xFFFF) {

closeConnection();

statusLabel→setText(tr("Found %1 trip(s)") .arg(listView→childCount()));

break;

}

if (socket.bytesAvailable() < blockSize)

break;

QDate date;

QTime departureTime;

QTime arrivalTime;

Q_UINT16 duration;

Q_UINT8 changes;

QString trainType;

in >> date >> departureTime >> duration >> changes >> trainType;

arrivalTime = departureTime.addSecs(duration * 60);

new QListViewItem(listView, date.toString(LocalDate),

departureTime.toString(tr("hh:mm")), arrivalTime.toString(tr("hh:mm")),

tr("%1 hr %2 min").arg(duration / 60).arg(duration % 60),

QString::number(changes), trainType);

blockSize = 0;

}

}

updateListView()처리부는 QSocket가 봉사기로부터 새 자료를 수신할 때마다 발생되는 QSocket의 readyRead()신호와 련결된다. 처음으로 할 일은 단일발사련결시계를 재기동하는것이다. 봉사기로부터 자료를 수신할 때마다 련결이 살아있다는것을 알고있으므로 시계가 30s동안 실행되도록 설정한다.

봉사기는 사용자의 기준에 맞는 가능한 렬차려행목록을 송신한다. 그 매개 려행은 단일블로크로서 전송되고 매개 블로크는 크기로 시작된다. for순환의 코드가 복잡한것은 봉사기로부터 한번에 1개 자료블로크를 꼭 얻지 못하는데 있다. 블로크전체 혹은 블로크의 일부 혹은 1.5개 블로크, 지어는 모든 블로크들을 한번에 수신할수 있다.

blockSize변수가 0이면 이것은 다음 블로크의 크기를 읽지 못했다는것을 의미하므로 그것을 읽으려고 한다.(읽을수 있는것이 적어도 2byte 있다고 가정한다.) 봉사기는 값 0xFFFF를 사용하여 받을 자료가 더는 없다는것을 지정하므로 이 값을 읽어들이면 끝에 이르렀다는것을 알게 된다.

블로크크기가 0xFFFF아니면 다음 블로크를 읽으려고 시도한다. 우선 읽을수 있는 블로크크기 byte가 있는가 알아보려고 한다. 없으면 거기서 중지한다. 유효자료가 있으면 readyRead()신호가 다시 발생되고 그다음 다시 시도한다. 블로크전체가 도착했다는것이 확실하면 QSocket에 설정한 QDataStream에 대하여 >>연산자를 리용하여 려행과 관련한 정보를 안전하게 꺼내고 그 정보를 리용하여 QListViewItem을 창조한다.

끝으로 blockSize변수를 0으로 재설정하여 다음 블로크의 크기가 알려지지 않았고 읽어들여야 한다는것을 가리킨다.

void TripPlanner::closeConnection() {

socket.close();

searchButton→setEnabled(true); stopButton→setEnabled(false);

connectionTimer.stop();

progressBarTimer.stop(); progressBar→setProgress(0);

}

closeConnection()비공개함수는 TCP봉사기에로의 련결을 닫고 사용자대면부를 갱신하고 시계들을 정지시킨다. 이 함수는 0xFFFF를 읽어들일 때 updateListView()로부터 호출되며 간단히 설명하는 다른 처리부들로부터도 호출된다.

void TripPlanner::stopSearch(){

statusLabel→setText(tr("Search stopped"));

closeConnection();

}

stopSearch()처리부는 Stop단추의 clicked()신호에 련결된다. 본질상 이것은 closeConnection()를 호출한다.

void TripPlanner::connectionTimeout(){

statusLabel→setText(tr("Error: Connection timed out"));

closeConnection();

}

connectionTimeout()처리부는 connectionTimer의 timeout()신호에 련결된다.

void TripPlanner::connectionClosedByServer() {

if (blockSize != 0xFFFF)

statusLabel→setText(tr("Error: Connection closed by server"));

closeConnection();

}

connectionClosedByServer()처리부는 소케트의 connectionClosed()신호에 련결된다.

Trip Planner응용프로그람의 main()함수는 다음과 같다.

int main(int argc, char *argv[]){

QApplication app(argc, argv);

TripPlanner tripPlanner;

app.setMainWidget(&tripPlanner);

tripPlanner.show();

return app.exec();

}

그러면 봉사기를 실현하자. 봉사기는 2개의 클라스 즉 TripServer와 ClientSocket로 이루어진다. TripServer클라스는 들어오는 TCP련결을 받아들이는 클라스 QServerSocket를 계승한다.

ClientSocket는 QSocket를 재정의하며 단일련결을 처리한다. 임의의 시간에 기억기에는 봉사받고있는 의뢰기로서 많은 ClientSocket객체가 있을수 있다.

TripServer클라스는 QServerSocket로부터 newConnection()함수를 재정의한다. 이 함수는 봉사기가 요구를 받으려는 포구에 의뢰기가 련결하려고 시도할 때마다 호출된다.

TripServer::TripServer(QObject *parent, const char *name)

: QServerSocket(6178, 1, parent, name) {}

TripServer구성자에서는 포구번호(6178)를 기초클라스구성자에 넘긴다. 둘째 인수 1은 허용련결수이다.

void TripServer::newConnection(int socketId){

ClientSocket *socket = new ClientSocket(this);

socket→setSocket(socketId);

}

newConnection()에서는 ClientSocket객체를 TripServer객체의 자식으로 창조하고 그 소케트 ID를 주어진 수로 설정한다.

ClientSocket클라스는 QSocket를 계승하며 단일의뢰기의 상태를 밀봉한다.

ClientSocket::ClientSocket(QObject *parent, const char *name) : QSocket(parent,name) {

connect(this, SIGNAL(readyRead()), this, SLOT(readClient()));

connect(this, SIGNAL(connectionClosed()), this, SLOT(deleteLater()));

connect(this, SIGNAL(delayedCloseFinished()), this, SLOT(deleteLater()));

blockSize = 0;

}

구성자에서는 필요한 신호–처리부련결을 확립하고 blockSize변수를 0으로 설정하여 의뢰기로부터 보내온 블로크크기를 아직 모른다는것을 가리킨다.

connectionClosed()와 delayedCloseFinished()신호는 Qt의 사건순환고리에로 조종이 돌아올 때 객체를 삭제하는 QObject계승함수 deleteLater()에 련결된다. 이것은 동료에 의해 련결이 닫길 때 혹은 지연된 닫기를 완료할 때 ClientSocket객체가 삭제된다는것을 담보한다.

void ClientSocket::readClient() {

QDataStream in(this);

in.setVersion(5);

if (blockSize == 0) {

if (bytesAvailable() < sizeof(Q_UINT16))

return;

in >> blockSize;

}

if (bytesAvailable() < blockSize)

return;

Q_UINT8 requestType;

QString from;

QString to;

QDate date;

QTime time;

Q_UINT8 flag;

in >> requestType;

if (requestType == 'S') {

in >> from >> to >> date >> time >> flag;

srand(time.hour() * 60 + time.minute());

int numTrips = rand() % 8;

for (int i = 0;i < numTrips;++i)

generateRandomTrip(from, to, date, time);

QDataStream out(this);

out << (Q_UINT16)0xFFFF;

}

close();

if (state() == Idle)

deleteLater();

}

readClient()처리부는 QSocket의 readyRead()신호에 련결된다. blockSize가 0이면 blockSize를 읽는것으로 시작하고 그렇지 않으면 그것을 이미 읽었으므로 그대신에 전체 블로크가 도달했는가 검사한다. 전체 블로크를 읽을 준비가 되였으면 읽어들인다. QSocket(this객체)에 대하여 직접 QDataStream을 사용하며 >>연산자에 의하여 마당을 읽어들인다.

의뢰기의 요구를 읽었으면 응답을 생성할 준비가 된다. 이것이 실제현장에서 가동하는 응용프로그람이면 렬차시간표자료기지에서 정보를 검색하여 일치하는 렬차려행을 찾으려고 시도한다. 그러나 여기서는 우연적인 려행을 생성하는 generateRandomTrip()라는 함수로 충족시킨다. 이 함수를 우연회수로 호출하고 0xFFFF를 보내여 자료의 끝을 지정한다.

끝으로 련결을 닫는다. 소케트의 출력완충기가 비였으면 련결은 곧 끝나고 조종이 Qt의 사건순환고리로 돌아올 때 deleteLater()를 호출하여 이 객체를 삭제한다.(이것은 delete this보다 더 안전하다.) 그렇지 않으면 QSocket는 모든 자료전송을 끝내고 련결을 닫으며 delayedCloseFinished()신호를 발생한다.

void ClientSocket::generateRandomTrip(const QString &, const QString &, const QDate &date, const QTime &time) {

QByteArray block;

QDataStream out(block, IO_WriteOnly);

out.setVersion(5);

Q_UINT16 duration = rand() % 200;

out << (Q_UINT16)0 << date << time << duration

<< (Q_UINT8) 1 << QString("InterCity");

out.device()→at(0);

out << (Q_UINT16) (block.size() -sizeof(Q_UINT16));

writeBlock(block.data(), block.size());

}

generateRandomTrip()함수는 TCP련결에서 자료블로크를 송신하는 방법을 보여준다. 이것은 의뢰기의 sendRequest()함수에서 수행한것과 거의 비슷하다. 다시한번 블로크를 QByteArray에 써넣고 writeBlock()에 의해 송신하기 전에 크기를 결정할수 있다.

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

TripServer server;

if (!server.ok()) {

qWarning("Failed to bind to port");

return 1;

}

QPushButton quitButton(QObject::tr("&Quit"), 0);

quitButton.setCaption(QObject::tr("Trip Server"));

app.setMainWidget(&quitButton);

QObject::connect(&quitButton, SIGNAL(clicked()), &app, SLOT(quit()));

quitButton.show();

return app.exec();

}

main()에서는 TripServer객체와 사용자가 봉사기를 정지시킬수 있는 QPushButton을 창조한다.

이로서 의뢰기–봉사기실례를 끝낸다. 이 경우에 읽고쓰기에 QDataStream을 사용하는 블로크지향통신규약을 사용하였다. 행지향통신규약을 사용하려고 하는 경우에 가장 간단한 수법은 readyRead()신호에 련결된 처리부에서 QSocket의 canReadLine()과 readLine()함수를 사용하는것이다.

QStringList lines;

while (socket.canReadLine())

lines.append(socket.readLine());

그다음 읽어들인 매 행을 처리한다. 자료전송에서와 같이 이것은 QSocket에서 QTextStream을 사용하여 수행한다.

### 4. QSocketDevice를 리용한 UDP망프로그람작성

QSocketDevice클라스는 TCP와 UDP에서 사용할수 있는 저수준대면부를 제공한다.대부분의 TCP응용프로그람들에서는 고수준QSocket클라스를 요구하지만 UDP를 사용하려면 직접 QSocketDevice를 사용해야 한다.

UDP는 믿음성없는 데이터그램지향통신규약이다. 일부 응용층통신규약들은 TCP보다 더 가벼운 UDP를 사용한다. UDP에서 자료는 한 주콤퓨터로부터 다른 주콤퓨터에로 파케트(데이터그램들)로서 송신된다. 거기에는 련결이란 개념이 없고 UDP파케트가 성공적으로 송달되지 않아도 체계에는 오유가 통보되지 않는다.

Weather Balloon과 Weather Station실례를 통하여 Qt응용프로그람으로부터 UDP의 사용법을 알게 된다. Weather Balloon응용프로그람은 5s간격으로 현재 대기조건을 포함하는 UDP데이터그램을 보내는 비GUI응용프로그람이다. Weather Station응용프로그람은 이 데이터그램들을 수신하여 화면에 현시한다. Weather Balloon의 코드를 서술하는것부터 시작한다.

WeatherBalloon클라스는 QPushButton을 계승한다. 이것은 Weather Station과 교제하는데 그 QSocketDevice비공개변수를 사용한다.

WeatherBalloon::WeatherBalloon(QWidget *parent, const char *name)

: QPushButton(tr("Quit"), parent, name), socketDevice(QSocketDevice::Datagram){

socketDevice.setBlocking(false);

myTimerId = startTimer(5 * 1000);

}

구성자의 초기화목록에서는 QSocketDevice::Datagram을 QSocketDevice구성자에 넘기여 UDP소케트장치를 창조한다. 구성자본체에서는 setBlocking(false)를 호출하여 QSocketDevice를 비동기로 만든다.(기정으로 QSocketDevice는 동기적이다.)

startTimer()를 호출하여 5s간격으로 시계사건을 생성한다.

void WeatherBalloon::timerEvent(QTimerEvent *event) {

if (event→timerId() == myTimerId) {

QByteArray datagram;

QDataStream out (datagram, IO_WriteOnly);

out.setVersion(5);

out << QDateTime::currentDateTime() << temperature() << humidity() <<altitude();

socketDevice.writeBlock(datagram, datagram.size(), 0x7F000001, 5824);

} else

QPushButton::timerEvent(event);

}

시계사건처리함수에서는 현재 날자, 시간, 온도, 습도, 표고를 포함하는 데이터그램을 생성한다.

데이터그램은 writeBlock()에 의해 송신된다. writeBlock()의 셋째와 넷째 인수는 IP주소와 동료(Weather Station)의 포구번호이다. 이 실례에서는 Weather Balloon과 같은 콤퓨터에서 Weather Station를 실행하고있다고 가정하므로 국부주콤퓨터를 지정하는 특수 IP주소인 127.0.0.1(0x7F000001)을 사용한다. QSocket와 달리 QSocketDevice는 주콤퓨터이름을 받아들이지 않고 주콤퓨터번호만 받아들인다. 여기서 주콤퓨터이름을 IP주소로 해결하려고 한다면 QDns클라스를 사용해야 한다.

보통과 같이 main()함수가 필요하다.

int main(int argc, char *argv[]) {

QApplication app(argc, argv);

WeatherBalloon balloon;

balloon.setCaption(QObject::tr("Weather Balloon"));

app.setMainWidget(&balloon);

QObject::connect(&balloon, SIGNAL(clicked()), &app, SLOT(quit()));

balloon.show();

return app.exec();

}

main()함수는 단순히 WeatherBalloon객체를 창조하고 이 객체는 UDP동료로서 그리고 화면우의 QPushButton으로서 모두 작업한다. QPushButton을 찰칵하여 사용자는 응용프로그람을 중지할수 있다.

QSocketDevice클라스는 봉사기에서 어느 주소와 포구에 응답하는가를 결정하는데 사용하는 peerAddress()와 peerPort()함수를 가지고있다.

## 제4절. XML

XML(Extensible Markup Language)은 자료교환과 자료보관에서 큰 인기를 끌고있는 본문화일형식이다.

Qt는 XML문서를 처리하기 위한 2가지 다른 API를 제공한다.

·SAX(Simple API for XML)는 가상함수들을 통하여 응용프로그람에 직접 사건해석을 통보한다.

·DOM(Document Object Model)은 XML문서를 응용프로그람이 항행할수 있는 나무구조로 변환한다.

특정한 응용프로그람에서 DOM과 SAX중 하나를 선택할 때 고려해야 할 인자들이 많다.

SAX는 준위가 낮고 보통 빠르다. 이것은 단순한 과제들(XML문서에서 주어진 꼬리표의 출현을 모두 찾는것 등)과 기억기를 많이 소비하는 대규모화일들을 읽어들이는데 특히 적합하다.

그러나 대부분의 응용프로그람들에서 DOM이 제공하는 편리성은 SAX의 잠재적인 속도와 기억기리득보다 더 크다.

### 1. SAX에 의한 XML읽기

SAX는 사실상 XML문서들을 읽어들이기 위한 공개적인 표준Java API이다. Qt의 SAX클라스들은 SAX2 Java실현후에 모형화되고 Qt관례에 일치시켰으므로 좀 차이가 있다.

Qt는 QXmlSimpleReader라고 부르는 SAX에 기초하는 비합법적인 XML문장해석기를 제공한다. 이 문장해석기는 잘 형식화된 XML을 인식하고 XML이름공간들을 유지한다. 문장해석기가 문서를 읽어들일 때 등록된 처리함수클라스들의 가상함수들을 호출하여 문장해석사건들을 가리킨다.(이 《문장해석사건》들은 건과 마우스사건들과 같은 Qt사건들에 관련되지 않는다.) 례를 들면 문장해석기가 다음의 XML문서를 해석하고있다고 가정한다.

<doc>

<quote>Errare humanum est</quote>

</doc>

문장해석기는 다음과 같은 문장해석사건처리함수들을 호출한다.

startDocument()

startElement("doc")

startElement("quote")

characters("Errare humanum est")

endElement("quote")

endElement("doc")

endDocument()

우의 함수들은 모두 QXmlContentHandler에서 선언된다. 단순성을 위하여 startElement()와 endElement()의 일부 인수들을 생략하였다.

QXmlContentHandler는 QXmlSimpleReader와 결합하여 사용할수 있는 수많은 처리함수클라스들중 하나이다. 그밖에 QXmlEntityResolver, QXmlDTDHandler, QXmlError Handler, QXmlDeclHandler, QXmlLexicalHandler가 있다. 이러한 클라스들은 오직 순수가상함수들만 선언하며 각종 문장해석사건들에 대한 정보를 준다. 대부분의 응용프로그람들에서는 오직 QXmlContentHandler와 QXmlErrorHandler 두개만 요구한다.

또한 편리상 Qt는 다중계승을 통하여 모든 처리함수클라스들을 계승하며 모든 함수들의 일반적실현을 주는 QXmlDefaultHandler클라스를 제공한다. 이 설계는 많은 추상처리함수클라스들과 하나의 일반파생클라스를 가지는데 이것은 일반적으로 Qt가 아니라 Java실현모형에 기초하고있다.

이제는 QXmlSimpleReader와 QXmlDefaultHandler를 사용하여 특별한 XML화일형식을 해석하고 그 리용을 QListView에 표시하는 방법을 보여주는 실례를 고찰한다. QXmlDefaultHandler파생클라스를 SaxHandler라고 하고 그 처리형식은 색인항목과 보조항목들을 가지는 도서색인이다.

<?xml version="1.0"?>

<bookindex>

<entry term="sidebearings">

<page>10</page>

<page>34-35</page>

<page>307-308</page>

</entry>

<entry term="subtraction">

<entry term="of pictures">

<page>115</page>

<page>244</page>

</entry>

<entry term="of vectors">

<page>9</page>

</entry>

</entry>

</bookindex>

문장해석기를 실현하는 첫 단계는 QXmlDefaultHandler의 파생클라스를 만드는것이다.

Sax처리함수클라스는 QXmlDefaultHandler를 계승하며 4개의 함수 startElement(), endElement(), characters(), fatalError()를 재정의한다. 처음 3개 함수는 QXmlContentHandler에서 선언되고 마지막함수는 QXmlErrorHandler에서 선언된다.

SaxHandler::SaxHandler(QListView *view) { listView = view; currentItem = 0; }

SaxHandler구성자는 XML화일에 보관된 정보를 현시하려는 QListView를 받아들인다.

bool SaxHandler::startElement(const QString &, const QString &, const QString&qName, const QXmlAttributes &attribs) {

if (qName == "entry") {

if (currentItem) {

currentItem = new QListViewItem(currentItem);

} else {

currentItem = new QListViewItem(listView);

}

currentItem→setOpen(true);

currentItem→setText(0, attribs.value("term"));

} else if (qName == "page") {

currentText = "";

}

return true;

}

startElement()함수는 읽기프로그람이 새로운 열기꼬리표를 만날 때 호출된다. 셋째 파라메터는 꼬리표이름(혹은 더 정확하게는 그 《수식이름(qualified name)》)이다. 넷째 파라메터는 속성목록이다. 이 실례에서는 첫째와 둘째 파라메터들을 무시한다. 그것들은 XML의 이름공간기구를 사용하는 XML화일에 사용할수 있다.

꼬리표가 <entry>이면 새로운 QListView항목을 창조한다. 꼬리표가 다른 <entry>꼬리표안에 겹쌓이면 새 꼬리표는 색인안의 보조항목을 정의하고 둘러싸는 항목을 표시하는 QListViewItem의 자식으로서 QListViewItem을 창조한다. 그렇지 않으면 부모로서 listView를 가지는 QListViewItem을 창조하여 그것을 제일 웃준위항목으로 만든다. 항목에 대하여 setOpen(true)를 호출하여 그 자식들을 표시하고 setText()를 호출하여 렬 0에 표시된 본문을 <entry>꼬리표의 항속성의 값으로 설정한다.

꼬리표가 <page>이면 currentText를 빈 문자렬로 설정한다. currentText는 <page>와 </page>꼬리표들사이에 배치된 본문을 보관한다.

끝으로 true를 돌려주어 SAX에게 화일해석을 계속하라고 알린다. 알려지지 않은 꼬리표들을 오유로서 통보하려면 false를 돌려줄수 있다. 또한 그때 QXmlDefaultHandler로부터 errorString()를 재정의하여 적당한 오유통보문을 돌려준다.

bool SaxHandler::characters(const QString &str) {

currentText += str; return true;

}

characters()함수는 XML문서의 문자자료를 알리기 위하여 호출된다. 간단히 문자들을 currentText변수에 추가한다.

bool SaxHandler::endElement(const QString &, const QString &, const QString &qName) {

if (qName == "entry") {

currentItem = currentItem→parent();

} else if (qName == "page") {

if (currentItem) {

QString allPages = currentItem→text(1);

if (!allPages.isEmpty())

allPages += ", ";

allPages += currentText;

currentItem→setText(1, allPages);

}

}

return true;

}

endElement()함수는 읽기프로그람이 닫기꼬리표를 만날 때 호출된다. startElement()에서와 같이 셋째 파라메터는 꼬리표이름이다.

꼬리표가 </entry>이면 currentItem비공개변수를 갱신하여 현재 QListViewItem의 부모를 가리킨다. 이것은 currentItem변수가 대응하는 </entry>꼬리표를 읽기 전에 보관한 값을 되살리도록 한다.

꼬리표가 </page>이면 지정된 페지번호를 추가하거나 1렬 현재 항목의 본문에서 반점으로 구분된 목록까지의 페지범위를 추가한다.

bool SaxHandler::fatalError(const QXmlParseException &exception) {

qWarning("Line %d, column %d: %s", exception.lineNumber(), exception.columnNumber(), exception.message().ascii());

return false;

}

fatalError()함수는 읽기프로그람이 XML화일의 문장해석에서 실패할 때 호출된다. 이런 일이 생기면 단순히 행번호, 렬번호, 문장해석기의 오유를 주는 경고를 출력한다.

이로서 Sax처리함수클라스의 실현을 끝낸다. 그러면 클라스의 사용방법을 론의하자.

bool parseFile(const QString &fileName) {

QListView *listView = new QListView(0);

listView→setCaption(QObject::tr("SAX Handler"));

listView→setRootIsDecorated(true);

listView→setResizeMode(QListView::AllColumns);

listView→addColumn(QObject::tr("Terms"));

listView→addColumn(QObject::tr("Pages"));

listView→show();

QFile file(fileName);

QXmlSimpleReader reader;

SaxHandler handler(listView);

reader.setContentHandler(&handler); reader.setErrorHandler(&handler);

return reader.parse(&file);

}

2개 렬을 가지도록 QListView을 설정한다. 그다음 읽으려는 화일용으로 QFile객체를 창조하고 화일을 해석하려는 QXmlSimpleReader를 창조한다. QFile을 자체로 열 필요는 없고 Qt가 자동적으로 연다.

끝으로 SaxHandler객체를 창조하고 그것을 읽기프로그람에 대하여 내용처리함수와 오유처리함수의 두 처리함수로 설치하고 읽기프로그람에 대하여 parse()를 호출하여 문장해석을 수행한다.

SaxHandler에서는 오직 QXmlContentHandler와 QXmlError처리함수클라스로부터 함수들을 재정의한다. 다른 처리함수클라스로부터 함수들을 실현하였다면 읽기기구에 대하여 대응하는 설정함수들을 호출해야 한다.

### 2. DOM에 의한 XML읽기

DOM은 W3C(World Wide Web Consortium)에 의해 개발된 XML해석용 표준API이다. Qt는 XML문서들을 읽고 조작하고 쓰기 위한 비합법적인 DOM준위2실현을 제공한다.

DOM은 XML화일을 기억기에 나무로 표시한다. 필요할 때 DOM나무를 항행할수 있고 나무를 수정하여 디스크에 XML화일로 보관할수 있다.

다음과 같은 XML문서를 론의하자.

<doc>

<quote>Errare humanum est</quote>

<translation>To err is human</translation>

</doc>

DOM나무는 각이한 형의 마디들을 포함한다. 례를 들면 Element마디는 열기꼬리표와 그와 짝을 이루는 닫기꼬리표에 대응한다. 꼬리표들사이에 놓이는 자료는 Element마디의 자식마디들로 표시된다.

Qt에서 마디형들은 다른 모든 DOM관련클라스들처럼 QDom앞붙이를 가진다. 이리하여 QDomElement는 Element마디를, QDomText는 Text마디를 각각 표시한다.

각이한 형의 마디들은 각종 자식마디를 가질수 있다. 례를 들면 Element마디는 다른 Element마디들과 또한 EntityReference, Text, CDATASection, ProcessingInstruction 그리고 Comment마디들을 포함할수 있다.

DOM을 리용하여 XML화일을 읽는 방법을 설명하기 위하여 도서색인화일형식용의 문장해석기를 쓴다.

도서색인 XML문서를 해석하는 DomParser라는 클라스를 정의하고 QListView에 결과를 현시한다. 이 클라스는 다른 클라스를 계승하지 않는다.

DomParser::DomParser(QIODevice *device, QListView *view){

listView = view;

QString errorStr;

int errorLine;

int errorColumn;

QDomDocument doc;

if (!doc.setContent(device, true, &errorStr, &errorLine, &errorColumn)) {

qWarning("Line %d, column %d: %s", errorLine, errorColumn, errorStr.ascii());

return;

}

QDomElement root = doc.documentElement();

if (root.tagName() != "bookindex") {

qWarning("The file is not a bookindex file");

return;

}

QDomNode node = root.firstChild();

while (!node.isNull()) {

if (node.toElement().tagName() == "entry")

parseEntry(node.toElement(), 0);

node = node.nextSibling();

}

}

구성자에서는 QDomDocument객체를 창조하고 그것에 대하여 setContent()를 호출하여 QIODevice가 제공하는 XML문서를 읽어들인다. setContent()함수는 장치가 이미 열려져 있지 않으면 그것을 자동적으로 연다. 그다음 QDomDocument에 대하여 document Element()를 호출하여 하나의 QDomElement자식을 얻고 그것이 <bookindex>요소인가 검사한다. 그다음 모든 자식마디들을 순환하면서 마디가 <entry>요소이면 parseEntry()를 호출하여 해석한다.

QDomNode클라스는 임의의 형의 마디를 보관할수 있다. 마디를 더 처리하려고 한다면 우선 마디를 정확한 자료형으로 변환해야 한다. 이 실례에서는 오직 Element마디들만 론의하므로 QDomNode에 대하여 toElement()를 호출하여 QDomElement로 변환한 다음 tagName()을 호출하여 요소의 꼬리표이름을 얻는다. 마디가 Element형이 아니면 toElement()함수는 빈 꼬리표이름을 가지는 빈 QDomElement객체를 돌려준다.

void DomParser::parseEntry(const QDomElement &element, QListViewItem *parent){

QListViewItem *item;

if (parent)

item = new QListViewItem(parent);

else

item = new QListViewItem(listView);

item→setOpen(true);

item→setText(0, element.attribute("term"));

QDomNode node = element.firstChild();

while (!node.isNull()) {

if (node.toElement().tagName() == "entry")

parseEntry(node.toElement(), item);

else if (node.toElement().tagName() == "page") {

QDomNode childNode = node.firstChild();

while (!childNode.isNull()) {

if (childNode.nodeType() == QDomNode::TextNode) {

QString page = childNode.toText().data();

QString allPages = item→text(1);

if (!allPages.isEmpty())

allPages += ", ";

allPages += page;

item→setText(1, allPages);

break;

}

childNode = childNode.nextSibling();

}

}

node = node.nextSibling();

}

}

parseEntry()에서는 QListView항목을 창조한다. 꼬리표가 다른 <entry>꼬리표안에 겹쌓이면 새 꼬리표는 색인안의 보조항목을 정의하고 둘러싸고있는 항목을 표시하는 QListViewItem의 자식으로서 QListViewItem을 창조한다. 그렇지 않으면 부모로서 listView를 가지는 QListViewItem을 창조하여 그것을 제일 웃준위항목으로 만든다. 그 항목에 대하여 setOpen(true)를 호출하여 보조항목을 볼수 있도록 하며 setText()를 호출하여 렬 0에 표시된 본문을 <entry>꼬리표의 term속성값으로 설정한다.

QListViewItem을 초기화한 다음 현재 <entry>꼬리표에 대응하는 QDomElement마디의 자식마디들을 순환한다.

요소가 <entry>이면 현재 항목을 둘째 인수로 하여 parseEntry()를 호출한다. 그때 새 항목의 QListViewItem은 둘러싸인 항목의 QListViewItem을 부모로 하여 창조된다.

요소가 <page>이면 요소의 자식목록을 항행하여 Text마디를 찾는다. 그것을 발견하였으면 toText()를 호출하여 QDomText객체로 변환하고 data()를 호출하여 본문을 QString으로서 꺼낸다. 그다음 그 본문을 QListViewItem의 1렬안에서 반점으로 구분한 목록에 추가한다.

그러면 DomParser클라스에 의하여 화일을 해석하는 방법을 론의하자.

void parseFile(const QString &fileName){

QListView *listView = new QListView(0);

listView→setCaption(QObject::tr("DOM Parser"));

listView→setRootIsDecorated(true);

listView→setResizeMode(QListView::AllColumns);

listView→addColumn(QObject::tr("Terms"));

listView→addColumn(QObject::tr("Pages"));

listView→show();

QFile file(fileName);

DomParser(&file, listView);

}

QListView의 설정으로 시작한다. 그다음 QFile과 DomParser를 창조한다. DomParser가 구성될 때 화일을 해석하고 목록보기를 채운다.

실례에서 설명하는것처럼 DOM나무항행은 힘들수 있다. <page>와 </page>사이의 본문을 간단히 발취하려면 firstChild()와 nextSibling()을 리용하여 QDomNodes목록을 순환할것을 요구한다.

### 3. XML쓰기

Qt응용프로그람들로부터 XML화일들을 생성하는데 기본적으로 2가지 수법이 있다.

·DOM나무를 구축하고 그것에 대하여 save()를 호출한다.

·코드를 작성하여 XML을 생성할수 있다.

이 수법들사이의 선택은 흔히 XML문서들을 읽어들이는데 SAX를 사용하는가 DOM을 사용하는가에 의존한다.

여기에 DOM나무를 창조하고 QTextStream에 의하여 그것을 써넣는 방법을 설명하는 코드부분이 있다.

const int Indent = 4;

QDomDocument doc;

QDomElement root = doc.createElement("doc");

QDomElement quote = doc.createElement("quote");

QDomElement translation = doc.createElement("translation");

QDomText quoteText = doc.createTextNode("Errare humanum est");

QDomText translationText = doc.createTextNode("To err is human");

doc.appendChild(root);

root.appendChild(quote); root.appendChild(translation);

quote.appendChild(quoteText);

translation.appendChild(translationText);

QTextStream out(&file);

doc.save(out, Indent);

save()의 둘째 인수는 사용하려는 들여쓰기를 나타낸다. 들여쓰기의 크기는 0아닌 값으로 설정하면 사람들이 화일을 읽기 쉽다. 여기에 XML화일출력이 있다.

<doc>

<quote>Errare humanum est</quote>

<translation>To err is human</translation>

</doc>

다른 대본은 DOM나무를 기본자료구조로 사용하는 응용프로그람들에 있다. 이러한 응용프로그람들은 보통 DOM을 리용하여 XML문서들을 읽어들인 다음 기억기에서 DOM나무를 수정하고 끝으로 save()를 호출하여 나무를 XML로 변환한다.

우의 실례에서는 부호화로서 UTF-8을 사용한다. DOM나무에 <?xml version="1.0" encoding="ISO-8859-1"?>를 종속시킴으로써 다른 부호화를 사용할수 있다. 다음의 코드부분은 이것을 수행하는 방법을 보여준다.

QTextStream out(&file);

QDomNode xmlNode = doc.createProcessingInstruction("xml","version=\"1.0\" encoding=\"ISO-8859-1\"");

doc.insertBefore(xmlNode, doc.firstChild());

doc.save(out, Indent);

수동적으로 XML화일들을 생성하여 DOM을 리용하는것보다 힘들지 않다.

QTextStream을 리용하여 문자렬들을 임의의 본문화일에 대하여 수행한것처럼 써넣을수 있다. 가장 엄격한 부분은 본문과 속성값들에서 특수문자들을 확장하는것이다. 개별적인 함수에서 이것을 수행할수 있다.

QString escapeXml(const QString &str) {

QString xml = str;

xml.replace("&", "&amp;"); xml.replace("<", "&lt;");

xml.replace(">", "&gt;"); xml.replace("'", "&apos;"); xml.replace("\"", "&quot;");

return xml;

}

여기에 그것을 사용하는 실례가 있다.

QTextStream out(&file);

out.setEncoding(QTextStream::UnicodeUTF8);

out << "<doc>\n" << " <quote>" << escapeXml(quoteText) << "</quote>\n"

<< " <translation>" << escapeXml(translationText) << "</translation>\n" << "</doc>\n"

## 제5절. 오려둠판기능

끌어다놓기조작(drag_and_drop)에서는 효과적인 리용자대면부가 제공된다.

끌어다놓기조작기능을 리용하면 응용프로그람안에서 또는 응용프로그람사이에서 자료의 넘기기를 진행할수 있다.

이와 함께 오림판(clipboard)에서는 또 다른 한가지 간단한 자료교환방식이 제공된다.

### 1. 끌어다놓기조작

#### 1) 끌어다놓기의 허용

끌어다놓기조작은 응용프로그람들사이에서 진행할수도 있고 응용프로그람안에서 진행할수도 있다.

Qt에서는 끌어다놓기조작인가를 정확히 알기 위하여 두개의 변수를 리용한다.

첫번째 변수는 QApplication::startDragTime으로서 리용자가 마우스단추를 얼마나 누르고있어야 끌어다놓기조작으로 인식하는가를 표시한다. 기정값으로 500㎳이다. 두번째 변수는 QApplication::startDragDistance로서 리용자가 마우스로 몇개의 화소만큼 이동시켜야 끌기조작으로 인식하는가를 표시한다. 기정값은 4개 화소이다. 일반적으로 이러한 기정값은 합리적이므로 변화시킬 필요는 없다.

끌어다놓기조작을 시작하기 위하여서는 QDrag대상을 만든 다음 이 대상의 성원함수 start()를 호출하여야 한다.

일반적으로 마우스단추를 눌러 일정한 거리만큼 움직인 다음 끌어다놓기조작을 시작하여야 한다.

이렇게 하면 보다 정확히 끌어다놓기조작을 식별할수 있다. 끌어다놓기조작은 창문부분품의 mousePressEvent()함수에 의하여 진행된다.

그 코드내용은 다음과 같다.

void MainWindow::mousePressEvent(QMouseEvent *event) {

if(event→button()＝＝Qt::LeftButton) {

QDrag *drag＝ndw QDrag(this);

QMimeData *mimeData＝new QMimeData;

mimeData→setText(textEdit→toPlainText());

drag→setMimeDAta(mimeData);

drag→setPixmap(dragPixmap);

Qt::DropAction dropAction＝drag→start();

....

}

}

프로그람에서 끌어다놓기하는 자료형태를 나타내기 위하여 QMimeData()대상을 리용한다. QMimeData는 MIME(Multipurpose Internet Mail Extention protocol)류형자료의 포함기(container)클라스이다. 오림판의 자료서술에서도 이 QMimeData를 리용한다.

start()함수는 끌기를 시작할 때 이 함수의 파라메터에 값을 넘겨 시작하는 끌어다놓기가 복사, 이동, 그밖의 조작인가를 표시한다. start()함수는 실행된 다음 실제적인 끌어다놓기동작을 설명하는 값을 돌려준다.

파라메터와 돌림값형은 모두 Qt::DropAction이다.

목표창문부분품이 끌어다놓기조작을 받아들이게 하기 위하여서는 setAcceptDrops (true)함수를 호출하여 창문부분품이 끌어다놓기를 접수하도록 하여야 한다. 이와 함께 두개의 사건처리함수 dragEnterEvent()와 dropEvent()를 실현하여야 한다.

dragEnterEvent()사건은 자료끌기가 목표창문부분품에 도착하였을 때 발생한다. 함수안에서 리용자는 끌어다놓기자료에 필요한 처리를 진행한다.

다음의 코드는 본문자료의 끌어다놓기만을 지원한다.

void Window::dragEnterEvent(QDragEnterEvent *event) {

if(event→mimeData()→hasFormat("text/plain"))

event→acceptProposedAction();

}

끌어다놓기자료를 접수하기 위하여서는 또한 dragMoveEvent()나 dropEvent()응답함수를 실행시켜야 한다.

dropEvent()함수는 받아들인 끌어다놓기자료를 해석하여 접수한 응용프로그람에 대응한 처리를 진행할것을 통지한다.

여기서는 작성한 화상열람기에 끌어다놓기조작을 첨가하여 끌어다놓기조작을 어떻게 리용하는가를 설명한다. 화일열람기에서는 화상화일을 끌어다놓기하여 열수 있다.

다음의 코드는 응용프로그람의뢰기창문에 끌기하여 들어가는 사건 dragEnterEvent(QDragEnterEvent *event)이다.

void ImageWidget::dragEnterEvent(QDragEnterEvent *event) {

if(event→mimeData()→hasUrls()){

QString localFile;

QRegExp rx("\\.(jpg|bmp|jpeg|png|xpm)$", Qt::CaseInsensitive);

foreach(QUrl url,event→mimeDAta()→urls()){

localFile＝url.toLocalFile();

if (rx.indexIn(localFile)>＝0){

event→accept();

return;

}

else

event→ignore();

}

}

else

event→ignore();

}

여기서 QMimeData클라스의 hasUrls()함수는 끌기한 자료가 URL클라스형(즉 MIME클라스형 text/uri－list)인가를 판단한다.

이 코드에서는 자기콤퓨터 화일만 처리하므로 함수 QUrl.toLocalFile()을 리용하여 자기콤퓨터의 경로만을 되돌리고 망경로는 없앤다.

정규표현식을 다시 리용하여 화일확장자가 jpg, bmp, jpeg, png, xpm인 화일을 고른다. 만일 요구조건이 만족하면 함수 accept()를 리용하여 끌어다놓기사건을 접수하고 그렇지 않으면 함수 ignore()를 리용하여 이 사건을 무시한다. 함수 ignore()는 마우스지시자의 모양을 끌기사건을 금지하는 모양으로 변화시킨다.

함수 dragMoveEvent()의 내용은 dragEvent()와 같다.

창문부분품이 drop사건에 응답하도록 하기 위하여서는 함수 dropEvent()를 실행시켜야 한다.

그 코드내용은 다음과 같다.

void ImageWidget::dropEvent(QDropEvent *event) {

if(event→mimeData()→hasUrls()) {

QString localFile;

QRegExp rx("\\.(jpg|bmp|jpeg|png|xpm)$",Qt:CaseInsensitinve);

foreach(QUrl url,event→mimeData()→urls()){

localFile＝url.toLocalFile();

if(rx.indexIn(localFile)>＝0) {

event→accept();

setPixmap(localFile);

return;

}

else

event→ignore();

}

}

else

event→ignore();

}

dropEvent()함수는 dragEnterEvent()와 기본적으로 같다. 그러나 setPixmap()함수를 리용하여 화상을 현시하는 부분만이 다르다.

#### 2) 사용자정의끌기형

자기식의 자료형을 끌어다놓기하는것을 실현하려면 MIME클라스형을 자체로 정의하여야 한다. 모든 자료는 QByteArray()의 문자배렬에 배치한다. 다음 자체로 정의한 자료류형을 리용하여 다음과 같은 코드를 작성한다.

QByteArray itemData;

QDataStrem dataStrem(&itemData,QIODevice::WriteOnly);

dataStream<<pixmap<<eent→pos();

QMimeData *mimeData＝new QMimeData;

mimeData→setData("application/mymimedata",itemData);

자료를 접수할 때에는 QByteArray를 리용하여 자료를 꺼낸 다음 QDataStream을 리용하여 자료를 읽는다.

QByteArray itemData＝event→mimeData()→data("application/mymimedata");

QDataStream dataStream(&itemData,QIODeveice::ReadOnly);

#### 3) Graphics View에서의 끌어다놓기조작

Graphics View에서 끌어다놓기조작은 QWidget에서와 약간 다르다.

무대(scene), 보이기(view), 그림요소들은 모두 자기식의 끌어다놓기사건을 처리할수 있다. QGraphicsView는 QWidget로부터 직접 계승되므로 QWidget의 끌어다놓기기능을 가지고있다. View창이 끌어다놓기조작을 받으면 이 사건을 Graphics View의 QGraphics SceneDragDropEvent사건으로 변환시킨 다음 무대에 넘겨준다. 무대는 이러한 사건을 조종하여 마우스위치의 그림요소에 발송한다.

그림요소를 무대에 끌어다놓으려면 QDrag대상을 하나 만들고 그 지시자(Pointer)를 이 창문부분품에 넘겨주어야 한다. 그다음 끌어다놓기조작을 진행한다.

끌어다놓기조작은 흔히 마우스의 누르기와 이동을 진행할 때에 발생하므로 mouse PressEvent()와 mouseMoveEvent()함수안에서 원시 창문부분품의 지시자를 얻을수 있다.

그 코드내용은 다음과 같다.

void MyItem::mousePressEvent(QGraphicsSceneMouseEvent *event) {

QMimeData *data＝new QMimeData;

Data→setHtml("<h1>ItemData<h1>");

QDrag drag(event→widget());

drag.setMimeData(data);

drag.start();

}

무대의 끌어다놓기조작을 하지 못하게 하려면 QGraphicsItem의 자식클라스안에서 QGraphicsScenedragEnterEvent()나 막으려는 다른 사건처리부를 새롭게 실현하여야 한다.

실례로 해전모의프로그람에 끌어다놓기기능을 첨가하여 Graphics View에서 끌어다놓기조작을 어떻게 리용하는가에 대하여 본다.

여기서는 같은 편 대상을 대방편 대상우에 끌어다놓아 같은 편이 대방의 대상에 공격을 진행한다는것을 표시하는 코드를 작성한다. 이와 함께 대방을 향하여 날아가는 빠른 공중대상을 만든다.

그림요소는 기정상태에서 끌어다놓기조작을 지원하지 않으므로 그림요소의 구성자함수안에 setAcceptDrops(true)를 삽입하고 그림요소의 마우스누르기사건을 실현하여 끌기를 시작하여야 한다.

void Target::mousePressEvent(QGraphicsSceneMouseEvent *event) {

if((m_attribute!＝US)) {

event→ignore(); return;

}

setCursor(Qt::CloseHandCursor);

QByteArray itemData;

QDataStream dataStream(&itemData, QIODevice::WriteOnly);

dataStream<<mapToParent(QPointF(0,0));

QMimeData *data＝new QMimeData;

Data→setData("application/x－dndtarget", itemDaa);

QDrag*drag＝new QDrag(event→widget());

Drag→setMimeData(data);

Drag→start();

}

여기서는 먼저 같은 편 대상인가를 판단하고 아니라면 끌기사건에 응답하지 않는다.

같은 편 대상이라면 끌어다놓기를 시작한 다음 마우스모양을 《꽉쥔 손》(Qt:: ClosedHandCursor)모양으로 바꾸고 리용자에게 조종권을 넘긴다. 여기서 끌어다놓기의 자료는 자체로 정의한 자료류형 x－dndtarget이고 내용은 우리편 대상의 무대자리표이다.

dragEnterEvent()함수는 끌어다놓기조작이 그림요소에서 진행되였을 때의 처리함수이다.

void Target::dragEnterEvent(QGraphicsSceneDragDropEvent *event) {

if(m_attribute!＝Foe)

event→ignore();

else if(event→mimeData()→hasFormat("application/x－dndtarget"))

event→accept();

else

event→ignore();

}

여기서는 현재 그림요소가 적편에 속하는가를 판단하고 아니라면 dragEnterEvent사건을 무시한다. 그렇지 않으면 끌어다놓기자료에 대한 유효성판단을 진행한다. 마지막으로 마우스단추를 놓을 때 dropEvent()함수가 호출된다.

void Target::dropEvent(QGraphicsSceneDragDropEvent *event) {

if(m_attribute!＝Foe)

event→ignore();

else if(event→mimeDAta()－.hasFormat("application/x－dndtarget")) {

QByteArray itemData＝event→mimeData()→data("application/x－dndtarget");

QDataStream dtaStream(&itemData, QIODevice::ReadOnly);

QPointF missile;

dataStream>>missile;

QPointF owner＝mapToParent(0,0);

qreal dx＝owner.x()－missile.x();

qreal dy＝owner.y()－missile.y();

qreal course＝atan(dy/dx);

QPointF test＝mapFromScene(missile);

if(((test.x()>0)&&(test.y()>0))||((test.x()>0)&&(test.y()<0)))

course＝Pi＋course;

Target*target＝new Target(12,course,Air,Us);

target→setPos(missile); target→setVisible(true);

scene()→addItem(target);

event→accept();

}

else

event→ignore();

}

함수안에서 공중대상을 새로 만들고 그의 각도를 계산하여 새로운 그림요소대상의 속성을 설정한 다음 이 그림요소를 무대안에 첨가한다.

### 2. 오림판의 리용

QClipboard클라스를 리용하면 창문체계의 오림판을 리용할수 있다.

QClipboard는 QDrag와 같은 자료류형을 지원한다.

QClipboard대상을 얻는 방법은 다음과 같다.

clipboard ＝ QApplication::clipboard();

Qt에서는 QMimeData클라스를 리용하여 오림판을 통해 교환되는 자료의 류형을 표시한다. 흔히 리용되는 자료들은 setText(), setImage(), setPixmap()함수를 리용하여 오림판에 보관할수 있다. 이러한 함수들은 QMimeData클라스안의 성원들과 류사하다. 다른 점은 QMimeData클라스성원은 자료가 기억되는 위치를 지정할수 있다는것이다. 만일 QClipboard::Clipboard에 보관하라고 지정하면 자료는 오림판에 보관되고 QClipboard:: Selection을 지정하면 자료는 마우스로 선택한 포함기안에 놓인다.

기정상태에서 자료는 오림판에 놓인다.

실례로 QLineEdit안의 문자를 오림판에 복사하려면 다음과 같이 하여야 한다.

clipboard→setText(lineEdit→text(), QClipboard::Clipboard);

이 함수에서 두번째 파라메터는 기정값이 오림판이므로 특별히 지정하지 않아도 된다.

오림판을 리용하여 서로 다른 MIME류형의 자료를 교환할수 있다.

QMimeData대상을 하나 만들고 setData()함수를 리용하여 자료를 보관한다.

마지막으로 setMimeData를 리용하여 자료를 오림판에 넣는다.

오림판의 밑층실현구조는 조작체계에 따라 다르다.

오림판자료에 변화가 생기면 QClipboard클라스는 dataChanged()신호를 내보낸다. 리용자는 이 신호를 리용하여 오림판의 변화정보를 얻을수 있다.

QDropMoveEvent에서는 끌어다놓기자료를 얻을수 없다.

다음은 화상열람기프로그람에 화상을 오림판에 복사하는 기능을 실현하여 어떻게 오림판을 리용하는가에 대하여 본다.

먼저 QAction대상을 만들어 복사사건을 처리한다.

그 코드내용은 다음과 같다.

copyAct＝new QAction(QIcon(":/images/copy.png"),rt("Copy"),this);

copyAct→setShortcut(QKeySequence::Copy);

connect(copyAct,SIGNAL(triggered()),this,SLOT(copy()));

다음 이 QAction을 차림표와 도구띠에 첨가하고 copyAct의 신호처리부함수 copy()를 다음과 같이 실현한다.

void MainWindow::copy() {

QPixmap pix＝imageWidget→getPixmap();

clipboard→setImage(pix.toImage());

}

# 제4장. Qt응용프로그람의 활용기술

## 제1절. 다중스레드

보통의 GUI응용프로그람들은 하나의 실행스레드를 가지며 한번에 하나의 조작을 수행한다. 사용자가 단일스레드응용프로그람에서 사용자대면부로부터 시간을 소비하는 조작을 호출하면 그 조작이 처리되는동안 대면부는 일반적으로 동결된다.

다중스레드 Qt응용프로그람에서 GUI는 자기의 스레드에서 실행되며 처리는 하나이상의 다른 스레드들에서 진행된다. 이것은 긴장한 처리를 하는 경우에도 응용프로그람들이 제각기 GUI를 가지게 한다. 다중스레드작성의 다른 하나의 리득은 다중처리소자콤퓨터들에서 서로 다른 스레드들을 동시에 각이한 처리소자들에서 실행하여 좋은 성능을 낼수 있다는것이다.

### 1. 스레드처리

Qt응용프로그람에서 다중스레드를 제공하는것은 간단하다. 즉 QThread의 파생클라스를 만들고 그의 run()함수를 재정의한다. 그 과정을 보여주기 위하여 우선 조작탁에 같은 본문을 반복 출력하는 아주 간단한 QThread의 파생클라스코드를 론의한다.

스레드클라스는 QThread를 계승하며 run()함수를 재정의한다. 이 클라스는 2개의 추가함수 setMessage()와 stop()을 제공한다.

stopped변수는 각이한 스레드들로부터 호출되고 필요할 때마다 새로 읽어들이는것을 확인하려고 하므로 volatile로 선언한다. volatile예약어를 생략하면 콤파일러는 변수호출을 최적화할수 있으나 부정확한 결과를 초래할수 있다.

Thread::Thread() { stopped = false; }

구성자에서 stopped를 false로 설정한다.

void Thread::run() {

while (!stopped)

cerr << messageStr.ascii();

stopped = false;

cerr << endl;

}

run()함수가 호출되면 스레드실행이 시작된다. stopped변수가 false인 경우에 함수는 조작탁에 주어진 통보문을 출력한다. 스레드는 조종이 run()함수를 벗어날 때 완료한다.

void Thread::stop() { stopped = true; }

stop()함수는 stopped변수를 true로 설정하여 run()이 조작탁에 대한 본문출력을 정지하게 한다. 이 함수는 임의의 스레드로부터 임의의 시간에 호출할수 있다. 실례에서는 bool에 대한 대입이 원자연산이라고 가정한다. 이것은 타당한 가정으로서 bool이 true나 false라는것을 고려한다.

QThread는 실행중에 있는 스레드의 실행을 완료하는 terminate()함수를 제공한다.

terminate()의 사용은 권고하지 않는다. 그것은 임의의 점에서 스레드를 정지시킬수 있고 후에 스레드에 그 자체를 삭제할 기회를 주지 않기때문이다. 여기서 수행하는것처럼 stopped변수와 stop()함수를 사용하는것이 늘 안전하다.

이제는 처음의 스레드와 함께 2개의 스레드 A와 B를 사용하는 자그마한 Qt응용프로그람에서 스레드클라스를 사용하는 방법을 론의한다.

ThreadForm클라스는 스레드형의 2개 변수와 단추들을 선언하며 기본사용자대면부를 제공한다.

ThreadForm::ThreadForm(QWidget *parent, const char *name) : QDialog(parent,name) {

setCaption(tr("Threads"));

threadA.setMessage("A"); threadB.setMessage("B");

threadAButton = new QPushButton(tr("Start A"), this);

threadBButton = new QPushButton(tr("Start B"), this);

quitButton = new QPushButton(tr("Quit"), this);

quitButton→setDefault(true);

connect(threadAButton, SIGNAL(clicked()), this, SLOT(startOrStopThreadA()));

connect(threadBButton, SIGNAL(clicked()), this, SLOT(startOrStopThreadB()));

connect(quitButton, SIGNAL(clicked()), this, SLOT(close()));

...

}

구성자에서는 setMessage()을 호출하여 첫 스레드는 "A"를, 둘째 스레드는 "B"를 반복 출력하게 한다.

void ThreadForm::startOrStopThreadA() {

if (threadA.running()) {

threadA.stop();

threadAButton→setText(tr("Start A"));

} else {

threadA.start();

threadAButton→setText(tr("Stop A"));

}

}

사용자가 스레드 A용의 단추를 찰칵할 때 startOrStopThreadA()는 스레드가 실행중에 있으면 정지하고 그렇지 않으면 스레드를 기동한다. 또한 단추의 본문을 갱신한다.

void ThreadForm::startOrStopThreadB() {

if (threadB.running()) {

threadB.stop();

threadBButton→setText(tr("Start B"));

} else {

threadB.start();

threadBButton→setText(tr("Stop B"));

}

}

startOrStopThreadB()의 코드는 아주 간단하다.

void ThreadForm::closeEvent(QCloseEvent *event) {

threadA.stop(); threadB.stop();

threadA.wait(); threadB.wait();

event→accept();

}

사용자가 Quit를 찰칵하거나 창문을 닫으면 실행중에 있는 스레드들을 정지하고 QCloseEvent::accept()를 호출하기 전에 그것들이 끝나기를 기다린다.(QThread::wait()를 사용한다.) 이것은 이 실례에서는 문제가 없다하더라도 응용프로그람이 깨끗한 상태에서 완료하도록 한다.

응용프로그람을 콤파일하려면 .pro화일에 다음 행을 추가해야 한다.

CONFIG += thread

이것은 qmake가 Qt서고의 스레드판을 사용하게 한다. 스레드화된 Qt서고를 건설하려면 -thread지령행선택을 넘기여 Unix와 Mac OS X에서 스크립트환경을 구성해야 한다.

Windows에서 Qt서고는 기정으로 스레드화된다. 또한 Windows의 조작탁에 프로그람의 출력이 나타나게 하려고 하므로 조작탁선택을 요구한다.

win32:CONFIG += console

응용프로그람을 실행하고 Start A를 찰칵하면 조작탁은 'A'들로 채워진다. Start B를 찰칵하면 'A'와 'B'들이 엇바뀌는 렬들이 출력된다. Stop A를 찰칵하면 오직 'B'들이 출력된다.

다중스레드 응용프로그람들에서 일반적인 요구는 여러개의 스레드들을 동기시키는것이다.

Qt는 이것을 수행하는 QMutex, QMutexLocker, QSemaphore 및 QWaitCondition클라스들을 제공한다.

QMutex클라스는 변수 혹은 코드부분을 보호하는 수단을 제공함으로써 오직 하나의 스레드를 한번에 호출할수 있다. 이 클라스는 Mutex를 잠그는 lock()함수를 제공한다. Mutex가 잠그어지지 않았으면 현재 스레드는 곧 그것을 포착하고 잠그며 그렇지 않으면 현재 스레드는 Mutex를 보유하는 스레드가 Mutex를 열 때까지 차단된다. 한편 lock()호출이 돌아올 때 현재 스레드는 unlock()를 호출할 때까지 Mutex를 보유한다. 또한 QMutex는 Mutex가 이미 잠그어져있으면 곧 돌아오는 tryLock()함수를 제공한다.

생산자에서는 하나의 《자유》바이트를 얻는것으로 시작한다. 완충기가 소비자가 아직 읽지 못한 자료로 꽉 차면 acquire()호출은 소비자가 자료를 소비하기 시작할 때까지 기다린다.

일단 그 바이트를 얻었다면 그것을 우연자료('A', 'C', 'G', 혹은 'T')로 채우고 그 바이트를 《사용된》바이트로 풀어놓음으로써 그것을 소비자스레드가 읽을수 있게 한다.

void Consumer::run() {

for (int i = 0; i < DataSize; ++i) {

acquire(usedSpace);

cerr << buffer[i % BufferSize];

release(freeSpace);

}

cerr << endl;

}

소비자에서는 《사용된》 바이트를 얻는것으로 시작한다. 완충기에 읽어들일 자료가 더는 없으면 acquire()호출은 생산자가 생성할 때까지 기다린다. 바이트를 얻었다면 그것을 출력하고 바이트를 《자유》바이트로서 풀어놓아 생산자가 다시 자료를 채울수 있게 한다.

int main() {

usedSpace += BufferSize;

Producer producer;

Consumer consumer;

producer.start(); consumer.start();

producer.wait(); consumer.wait();

return 0;

}

끝으로 main()에서 QSemaphore의 비직관적인 ＋, ＝연산자를 리용하여 《사용된》공간을 모두 얻는것으로 시작한다. 이것은 채쓰지 않은 부분을 소비자가 읽어들이지 않도록 한다.

그 다음 생산자와 소비자스레드들을 기동한다. 그때 생기는 현상은 생산자가 《자유》공간을 《사용된》공간으로 변환하고 그다음 소비자는 그것을 《자유》공간으로 역변환할수 있다는것이다.

프로그람을 실행할 때 조작탁에 100 000개의 'A', 'C', 'G', 'T'들의 우연렬을 써넣고 완료한다.

그때 수행하는 작업을 리해하기 위하여 출력장치에 써넣기를 금지하고 그대신에 생산자가 바이트를 생성할 때마다 'P'를 쓰고 소비자가 바이트를 읽을 때마다 'C'를 써넣는다. 그리고 될수록 간단히 모든 동작이 진행되도록 하기 위하여 DataSize와 BufferSize에 훨씬 더 작은 값을 사용할수 있다.

생산자와 소비자를 동기시키는 문제를 해결하는 다른 수법은 QWaitCondition과 QMutex를 사용하는것이다. QWaitCondition은 어떤 조건이 만족될 때 한 스레드가 다른 스레드들을 깨우게 한다. 이것은 오직 Mutex들에 의해서만 가능한것보다 더 정확한 조종을 허용한다. 그 동작을 보여주기 위하여 기다림조건들을 사용하여 생산자-소비자실례를 다시 시행한다.

const int DataSize = 100 000;

const int BufferSize = 4 096;

char buffer[BufferSize];

QWaitCondition bufferIsNotFull;

QWaitCondition bufferIsNotEmpty;

QMutex mutex;

int usedSpace = 0;

완충기외에도 2개의 QWaitCondition, 한개의 QMutex, 그리고 완충기안에 《사용된》 바이트가 몇개인가를 보관하는 변수를 하나 선언한다.

void Producer::run() {

for (int i = 0;i < DataSize;++i) {

mutex.lock();

while (usedSpace == BufferSize)

bufferIsNotFull.wait(&mutex);

buffer[i % BufferSize] = "ACGT"[ (uint)rand() % 4];

++usedSpace;

bufferIsNotEmpty.wakeAll();

mutex.unlock();

}

}

생산자에서는 완충기가 찼는가 검사하는것으로 시작한다. 다 찼으면 《완충기가 차지 않음.》조건이 성립하기를 기다린다. 조건이 만족되면 완충기에 1byte 써넣고 usedSpace를 증가시키고 《완충기가 비지 않음.》조건이 true로 되기를 기다리는 스레드를 잠재운다.

Mutex를 사용하여 usedSpace변수에 대한 모든 호출을 보호한다. QWaitCondition:: wait()함수는 잠건된 Mutex를 첫 인수로 가지며 현재 스레드를 차단하기 전에 Mutex를 돌려준다.

이 실례에서는 while순환

while(usedSpace == BufferSize)

bufferIsNotFull.wait(&mutex);을 if문으로 교체한다.

if (usedSpace == BufferSize) {

mutex.unlock();

bufferIsNotFull.wait();

mutex.lock();

}

그러나 이것은 하나이상의 생산자스레드를 허용하자마자 차단된다. 그것은 다른 생산자가 wait()호출후 곧 Mutex를 동결하고 《완충기가 차지 않음.》조건을 다시 false로 만들수 있기때문이다.

void Consumer::run() {

for (int i = 0;i < DataSize;++i) {

mutex.lock();

while (usedSpace == 0)

bufferIsNotEmpty.wait(&mutex);

cerr << buffer[i % BufferSize];

--usedSpace;

bufferIsNotFull.wakeAll();

mutex.unlock();

}

cerr << endl;

}

소비자는 생산자와 정반대로 작업한다. 즉 소비자는 《완충기가 비지 않음.》조건을 기다리며 《완충기가 차지 않음.》조건을 기다리는 스레드를 깨운다.

지금까지의 모든 실례에서 스레드들은 같은 대역변수들을 호출하였다. 그러나 일부 스레드응용프로그람들은 서로 다른 스레드들에서 각이한 값을 보유하는 대역변수를 가질 필요가 있다. 이것은 흔히 스레드국부기억(thread-local storage, TLS) 혹은 스레드고유기억(thread-specific data, TSD)이라고 부른다. QThread::currentThread()로부터 돌아오는 스레드 ID들을 건으로 하는 매프를 리용하여 그것을 꾸밀수 있지만 더 좋은 수법은 QThreadStorage<T>클라스를 사용하는것이다.

QThreadStorage<T>의 일반적인 용도는 고속완충기억기이다. 서로 다른 클라스들에서 제각기 캐쉬를 취함으로써 Mutex에서 잠그기, 열기가 가능한 기다림으로 인한 추가적인 부담을 피할수 있다.

캐쉬변수는 스레드마다 QMap<int, double>의 지적자를 하나 가진다.(일부 콤파일러들에서 문제가 있으므로 QThreadStorage<T>에서 형판형은 지적자형이여야 한다.) 특정한 스레드에서 캐쉬를 처음 리용할 때 hasLocalData()는 false를 돌려주고 QMap<int, double>객체를 창조한다.

캐쉬와 함께 QThreadStorage<T>는 대역오유상태변수(toerrno와 비슷하다.)에 쓰이며 한개 스레드에서의 수정이 다른 스레드들에 영향을 주지 않도록 한다.

### 2. GUI스레드와의 교제

Qt응용프로그람이 기동할 때 오직 하나의 스레드 즉 초기스레드가 실행중에 있다. 이것은 QApplication객체를 창조하고 그것에 대하여 exec()를 호출하게 하는 유일한 스레드이다. 이러한 리유로 보통 이 스레드를 GUI스레드로 취급한다. exec()호출후에 이 스레드는 사건을 기다리거나 사건을 처리한다.

GUI스레드는 QThread파생클라스의 객체를 창조하여 새로운 스레드들을 기동할수 있다. 새로운 스레드들은 서로 교제할 필요가 있으면 Mutex, Semaphore 혹은 기다림조건들과 함께 공유변수들을 사용할수 있다. 그러나 이 기술은 사건순환고리를 잠그고 사용자대면부를 동결할수 있으므로 GUI스레드와 교제하는데 사용할수 없다.

비GUI스레드가 GUI스레드와 교제하기 위한 대책은 사용자정의사건들을 사용하는것이다. Qt의 사건기구는 기본형과 함께 사용자정의사건형들을 정의하고 QApplication:: postEvent()를 리용하여 이 형의 사건들을 발송할수 있다. 더우기 postEvent()가 스레드에 안전하므로 임의의 스레드로부터 이 함수를 리용하여 GUI스레드에로 사건을 발송할수 있다.

그 동작을 설명하기 위하여 사용자가 화상의 회전, 크기조절, 색깊이변경을 가능하게 하는 기본화상처리프로그람인 Image Pro의 코드를 서술한다. 응용프로그람은 비GUI스레드를 리용하여 사건순환고리를 잠그지 않고 화상에 대한 조작을 수행한다. 이것은 큰 화상을 처리할 때 크게 차이난다. 비GUI스레드는 수행해야 할 과제 또는 《일괄처리》들의 목록을 가지며 사건들을 기본창문에 보내여 진척정형을 알린다.

ImageWindow::ImageWindow(QWidget *parent, const char *name)

:QMainWindow(parent, name) {

thread.setTargetWidget(this);

...

}

ImageWindow구성자에서는 비GUI스레드의 《목표창문부분품》을 ImageWindow로 설정한다.

이 스레드는 그 창문부분품에 진척정형사건들을 발송한다. 스레드변수는 Transaction Thread형이다. 그것을 간단히 설명한다.

void ImageWindow::flipHorizontally() {

addTransaction(new FlipTransaction(Horizontal));

}

flipHorizontally()처리부는 FlipTransaction을 창조하고 비공개함수 addTransaction()을 사용하여 그것을 등록한다. flipVertical(), resizeImage(), convertTo32Bit(), convertTo8Bit(), convertTo1Bit()함수들도 비슷하다.

void ImageWindow::addTransaction(Transaction *transact) {

thread.addTransaction(transact);

openAct→setEnabled(false); saveAct→setEnabled(false);

saveAsAct→setEnabled(false);

}

addTransaction()함수는 일괄처리를 비GUI스레드의 일괄처리기다림렬에 추가하고 일괄처리들을 진행하는동안 Open, Save, Save As작용을 금지한다.

void ImageWindow::customEvent(QCustomEvent *event) {

if ((int)event→type() == TransactionStart) {

TransactionStartEvent *startEvent = (TransactionStartEvent *)event;

infoLabel→setText(startEvent→message);

} else if ((int)event→type() == AllTransactionsDone) {

openAct→setEnabled(true); saveAct→setEnabled(true);

saveAsAct→setEnabled(true);

imageLabel→setPixmap(QPixmap(thread.image()));

infoLabel→setText(tr("Ready")); modLabel→setText(tr("MOD"));

modified = true;

statusBar()→message(tr("Done"), 2000);

} else

QMainWindow::customEvent(event);

}

customEvent()함수는 사용자정의사건들을 처리할수 있게 QObject로부터 재정의된다.TransactionStart와 AllTransactionsDone상수들은 transactionthread.h에서 다음과 같이정의된다.

enum { TransactionStart = 1001, AllTransactionsDone = 1002 };

Qt의 기본사건들은 1 000아래의 값을 가진다. 더 큰 값들은 사용자정의사건들에 사용될수 있다.

사용자정의사건들의 자료형은 사건형과 함께 void지적자를 보관하는 QEvent의 파생클라스 QCustomEvent이다. TransactionStart사건들에서는 추가자료성원을 보관하는 QCustomEvent의 파생클라스를 사용한다.

TransactionStartEvent::TransactionStartEvent() : QCustomEvent(TransactionStart){}

구성자에서는 TransactionStart상수를 기초클라스구성자에 넘긴다.

그러면 TransactionThread클라스를 론의하자.

TransactionThread클라스는 배경에서 일괄처리들을 하나씩 처리하고 실행하기 위하여 일괄처리의 목록을 유지관리한다.

void TransactionThread::addTransaction(Transaction *transact){

QMutexLocker locker(&mutex);

transactions.push_back(transact);

if (!running())

start();

}

addTransaction()함수는 일괄처리기다림렬에 일괄처리를 추가하고 그것이 이미 실행중에 있지 않으면 일괄처리스레드를 기동한다.

void TransactionThread::run(){

Transaction *transact;

for (;;) {

mutex.lock();

if (transactions.empty()) {

mutex.unlock();

break;

}

QImage oldImage = currentImage;

transact = *transactions.begin();

transactions.pop_front();

mutex.unlock();

TransactionStartEvent *event = new TransactionStartEvent;

event→message = transact→messageStr();

QApplication::postEvent(targetWidget, event);

QImage newImage = transact→apply(oldImage);

delete transact;

mutex.lock();

currentImage = newImage;

mutex.unlock();

}

QApplication::postEvent(targetWidget, new QCustomEvent(AllTransactionsDone));

}

run()함수는 일괄처리기다림렬을 순환하면서 apply()를 호출하여 매개 일괄처리를 차례로 실행한다. 일괄처리들과 currentImage성원변수에 대한 모든 호출은 Mutex에 의해 보호된다.

일괄처리가 기동할 때 TransactionStart사건을 목표창문부분품(ImageWindow)에 발송한다. 모든 일괄처리가 처리를 완료하였을 때 AllTransactionsDone사건을 발생한다.

Transaction클라스는 사용자가 화상에 대하여 조작하는 추상기초클라스이다. 이것은 3개의 파생클라스 FlipTransaction, ResizeTransaction, ConvertDepthTransaction을 가진다. FlipTransaction만 론의하는데 다른 2개 클라스들은 비슷하다.

FlipTransaction구성자는 방향(Horizontal 혹은 Vertical)을 지정하는 하나의 파라메터를 가진다.

QImage FlipTransaction::apply(const QImage &image) {

return image.mirror(orientation == Qt::Horizontal, orientation == Qt::Vertical);

}

apply()함수는 파라메터로 받아들이는 QImage에 대하여 QImage::mirror()를 호출하고 결과 QImage를 돌려준다.

QString FlipTransaction::messageStr() {

if (orientation == Qt::Horizontal)

return QObject::tr("Flipping image horizontally…");

else

return QObject::tr("Flipping image vertically…");

}

messageStr()는 조작이 진행되는동안 상태띠에 표시할 통보문을 돌려준다. 이 함수는 ImageWindow::customEvent()와 GUI스레드에서 호출된다.

실행이 오래 걸리는 조작들에서는 진척정형을 알릴 필요가 있다. 추가적인 사용자정의사건을 창조하고 일정한 퍼센트의 처리가 끝나면 그것을 발송함으로써 수행할수 있다.

### 3. 스레드안전클라스

함수는 서로 다른 스레드들로부터 동시에 안전하게 호출할수 있을 때 스레드안전함수라고 말한다. 2개의 스레드안전함수를 서로 다른 스레드들로부터 같은 공유자료에 대하여 호출한다면 결과가 늘 정의된다. 더 확장하여 클라스는 그의 모든 함수들이 서로 다른 스레드들로부터 지어는 같은 객체에 대하여 조작할 때에도 서로 간섭하지 않고 동시에 호출할수 있을 때 스레드안전클라스라고 말한다.

Qt의 스레드안전클라스들은 QThread, QMutex, QMutexLocker, QSemaphore, QThreadStorage<T> 및 QWaitCondition이다. 또한 다음의 함수들은 스레드안전함수이다. 즉 QApplication::postEvent(), QApplication::removePostedEvents(), QApplication::removePostedEvent() 및 QEventLoop::wakeUp()이다.

Qt의 대다수 비GUI클라스들은 좀 엄격한 요구를 만족시켜야 한다. 그것은 재입구가능(reentrant)이다. 클라스의 각이한 실례들을 각이한 스레드들에서 동시에 사용할수 있으면 그 클라스는 재입구가능이다. 그러나 여러 스레드들사이에서 동시에 같은 재입구가능객체를 호출하는것은 안전하지 못하고 그러한 호출은 Mutex에 의해 보호되여야 한다. 일반적으로 대역적으로 참고하지 않는 임의의 C++클라스 혹은 공유자료는 재입구가능이다.

QObject는 재입구가능이지만 Qt의 어느 QObject파생클라스도 재입구가능이 아니다. 이로부터 얻어지는 하나의 결론은 비GUI스레드로부터 창문부분품에 대하여 함수들을 직접 호출할수 없다는것이다. 비GUI스레드로부터 QLabel의 본문을 변경하려고 한다면 사용자정의사건을 GUI스레드에 발송하여 본문을 변경할것을 요구해야 한다.

delete에 의한 QObject삭제는 재입구가능이 아니다. 비GUI스레드로부터 QObject를 삭제하기 위하여 《기한부삭제》사건을 발송하는 QObject::deleteLater()을 호출해야 한다.

QObject의 신호-처리부기구는 임의의 스레드에서 사용될수 있다. 신호가 한개 스레드에서 발생될 때 거기에 련결된 처리부들은 즉시 호출되고 실행은 같은 스레드에서 발생하고 수신자객체가 창조되는 스레드에서는 발생하지 않는다. 이것은 신호와 처리부를 사용하여 다른 스레드들로부터 GUI스레드와 교제할수 없다는것을 의미한다.

QTimer클라스와 망프로그람작성클라스 QFtp, QHttp, QSocket 및 QSocketNotifier는모두 사건순환고리에 의존하므로 비GUI스레드에서 사용할수 없다. 유효한 단 하나의 망구축클라스는 가동환경에 고유한 망구축API들을 위한 저수준의 QSocketDevice이다.

일반적인 기술은 비GUI스레드에서 동기QSocketDevice를 사용하는것이다. 일부 프로그람작성자들은 QSocket(비동기적으로 작업한다.)를 사용하는 경우보다 코드를 더 단순하게 하고 비GUI스레드에서 작업함으로써 사건순환고리를 차단하지 않는다.

또한 Qt의 SQL과 OpenGL모듈은 다중스레드응용프로그람들에서 쓰일수 있으나 체계에 따라 변하는 자체의 제한을 가지고있다.

QImage, QString, 용기클라스들을 비롯한 Qt의 대다수 비GUI클라스들은 최적화기술로서 암시적 혹은 명시적공유를 사용한다. 이 클라스들은 복사구성자와 대입연산자들을 제외하고 재입구가능이다. 이러한 클라스들의 실례의 사본을 취할 때 오직 내부자료의 지적자가 복사된다. 이것은 여러개의 스레드들이 자료를 동시에 수정하려고 하는 경우에는 위험하다. 그러한 경우에 해결책은 암시적 혹은 명시적으로 공유된 클라스의 실례에 대입을 할 때 QDeepCopy<T>클라스를 사용하는것이다. 례를 들면

QString password;

QMutex mutex;

void setPassword(const QString &str){

mutex.lock();

password = QDeepCopy<QString>(str);

mutex.unlock();

}

## 제2절. 프로쎄스들사이 통신

### 1. QProcess의 리용

Qt의 QProcess클라스는 외부프로그람들을 기동시키고 그것들과 통신하는데 리용된다.

하나의 새로운 프로쎄스를 기동시키는 방법은 간단하다. 대기상태에 있는 프로그람의 이름과 기동파라메터를 start()함수에 넘겨주면 된다.

QObject *parent;

…

QString program=”tar”;

QStringList arguments;

arguments<<”-style”<<”motif”;

QProcess *myProcess=new QProcess(parent);

myProcess→start(program, arguments);

start()함수를 호출한 다음 myProcess는 《기동상태》에 들어간다. 이때 tar프로그람은 호출되지 않으며 표준입출력장치에 읽기, 쓰기를 할수 없다. 프로쎄스는 기동한 다음 《실행상태》에 들어가며 started()신호를 발생시킨다.

입출력에서 QProcess는 프로쎄스를 흐름형의 I/O장치로 인식하며 QTcpSocket를 리용하여 흐름형의 망련결에 대하여 읽기, 쓰기할 때와 같이 프로쎄스를 읽기, 쓰기한다. QIODevice::write()함수를 리용하여 기동한 프로쎄스의 표준입력장치에 자료를 쓸수 있다.

또한 QIODevice::read(), QIODevice::readLine(), QIODevice::getChar()함수로 이 프로쎄스의 표준출구장치로부터 자료를 읽을수 있다. QIODevice에서 계승된 QProcess를 QXmlReader의 자료원천으로(또는 QFtp에서 올리적재하는데 리용하는 자료를 만드는데) 리용할수 있다.

프로쎄스가 탈퇴할 때 QProcess는 초기상태에 들어가며 finished()신호를 발생시킨다.

void QProcess::finished(int exitCode, QProcess::ExitStatus exitStatus)신호는 프로쎄스의 실행이 끝날 때 발생한다. 여기서 첫번째 파라메터는 탈퇴코드이며 두번째 파라메터는 탈퇴상태이다. 이 2개의 파라메터값은 exitCode()함수와 exitStatus()함수를 호출하여 얻는다. 여기서 Qt가 정의한 프로쎄스《탈퇴상태》에는 2가지 경우(정상탈퇴와 프로쎄스의 파괴)가 있다. 정상탈퇴인 경우 대응값은 QProcess::NormalExit(값 0)이며 프로쎄스의 파괴인 경우 대응값은 QProcess::CrashExit(값 1)이다.

프로쎄스가 실행될 때 오유가 발생하면 QProcess는 error()신호를 발생시키며 error()함수를 호출하여 마지막에 발생한 오유의 류형을 되돌린다. 이때 state()함수로 프로쎄스의 상태를 찾아볼수 있다.

프로쎄스의 표준출구에는 이미 정의되여있는 2개의 출구통로가 있다. 하나는 표준출구통로 stdout이다. 이것은 조종탁에서 출구하는데 리용된다. 다른 하나는 표준오유통로 stderr이다. 이것은 프로쎄스가 오유인쇄를 하는데 리용된다. 이 2개의 통로는 본질적으로 2개의 독립적인 자료흐름이다.

Qt는 setReadChannel()함수를 호출하여 현재의 읽기통로를 설정하며 읽기가능한 자료가 있을 때 readyRead()신호를 발생시킨다. 또한 읽기가능한 자료가 표준출구자료이면 동시에 readyReadStandardOutput()신호를 발생시키며 읽기가능한 자료가 표준오유자료이면 동시에 readyReadStandardError()신호를 발생시킨다. readyAllStandardOutput()함수와 readyAllStandardError()함수를 각각 호출하여 표준출구통로와 표준오유통로에서 자료를 읽는다. 이밖에 QProcess는 표준출구통로와 표준오유통로를 다같이 리용하도록 하는데 이때 리용하는 통로는 표준출구통로이다. 이 통로는 프로쎄스가 기동하기 전에MergedChannels파라메터로 setReadChannelMode()함수를 호출하는 방법으로 리용한다.

프로쎄스의 출구통로는 QProcess의 읽기통로에 대응되며 입구통로는 QProcess의 쓰기통로에 대응된다. 하나의 tar프로쎄스를 기동시키고 어떤 경로의 모든 내용들을 여벌복사로 묶는 프로그람은 다음과 같다.

int main(int argc, char **argv) {

QApplication app(argc, argv);

if (app.arguments().count()!=2) {

qDebug()<<QObject::tr(“Need a parameter for backup path ex:’ process/home’”);

return -1;

}

QProcess proc;

QStringList arguments;

arguments<<”czvf”<<”back.tar.gz”; arguments<<app.arguments().at(1);

proc.start(“tar”, arguments);

if (!proc.waitForStarted())

return false;

proc.closeWriteChannel();

QByteArray procOutput;

while(!proc.waitForFinished(0)){

if (proc.waitForReadyRead(10)){

procOutput=proc.readAll();

qDebug()<<procOutput;

}

}

return EXIT_SUCCESS;

}

이 프로그람에서는 반드시 여벌(backup)경로를 파라메터로 하여야 한다. 례를 들어 “process/home”을 여벌경로로 한다.

먼저 파라메터의 개수가 정확한가를 검사한다. 즉 app.arguments().count()가 “2”인가를 본다. 여기서 주의할것은 main()함수와 마찬가지로 arguments()함수는 프로그람자체를 0번째 파라메터로 간주하기때문에 파라메터를 계수할 때 프로그람도 포함시킨다는것이다. 그러므로 여기서는 count()값이 “2”로 된다. 그다음 파라메터(여벌자료의 경로)는 app.arguments().at(1)함수를 리용하여 얻는다. 파라메터검사를 한 다음 새로운 QProcess객체를 창조하고 이 프로그람의 파라메터표 arguments()를 만든다.

파라메터순서에 따라 선택항목 “czvf”, 현재 목록에 있는 package화일이름 “back.tar.gz”, app.arguments().at(1)에서 얻은 여벌경로이름을 파라메터표에 넘겨준다.

함수 proc.start(“tar”, arguments)로 tar프로쎄스를 기동시킨다.

waitForStarted()함수가 true값을 되돌린 다음 프로그람은 정상으로 실행된다. 새로 기동한 tar프로쎄스에는 자료를 입력하지 않는다. 그러므로 프로쎄스는 먼저 출구통로를닫는다. 그러나 프로쎄스의 출력정보를 얻기 위하여 프로쎄스는 while순환을 리용하여sub프로쎄스의 실행이 끝났는가를 검사한다. 만일 이 프로쎄스의 실행이 끝나지 않았으면sub프로쎄스의 모든 정보를 읽어들여 조종탁에 출력한다.

이때 리용하는 waitForFinished()함수는 프로쎄스가 끝나기를 기다리는것을 막는 기능을 하며 waitForReadyRead()함수는 자료읽기를 기다리는것을 막는 기능을 한다. 이 함수들이 가지는 파라메터는 막기시간(㎳단위)을 나타낸다.

### 2. D-Bus

#### 1) D-Bus의 개념

D-Bus는 프로쎄스사이의 통신(IPC:Inter Process Communication) 및 원격수속호출(RPC:Remote Procedure Call)기구이다. D-Bus는 체계급프로쎄스와 일반리용자 프로쎄스사이의 통신을 지원하도록 설계되여있다. 고속2진수정보전달규약인 D-Bus는 호출시간이 짧고 원가가 적게 들기때문에 국부통신에 많이 리용된다.

D-Bus에는 2개의 모선(체계모선, 대화조종모선)이 있다.

체계모선(system bus)은 조작체계나 배후프로쎄스에 의해 리용되는데 안정성이 높다. 대화조종모선(session bus)은 동시에 여러개가 있을수 있다. 이 대화조종모선들은 리용자가 접속한 다음 기동하는데 접속리용자에게만 속하여 리용자프로그람사이의 통신에 리용된다. 만일 프로그람이 체계모선으로부터 정보를 받아야 할 때 직접 체계모선에 련결할수 있다. 그러나 이때 발송허가된 정보는 발송제한을 받는다. 모선통신을 진행할 때 프로그람은 리용가능한 다른 객체를 얻고 봉사를 받을수 있다. 동시에 프로그람자체도 다른 프로그람이 요구하는 객체로 될수 있다. 모선은 통신요구가 “many to many”인 경우에 적용된다. D-Bus는 동시에 프로그람들사이의 직접통신도 지원한다.

저준위프로그람들은 통보(message)를 교환하는 방법으로 통신을 진행한다. 통보는 원격수속호출과 응답, 그에 따르는 오유를 중계(relay)하는데 리용된다. 모선을 리용할 때 통보는 하나의 목적주소를 가지는데 통보가 어떤 원인(례를 들어 “swarming” 또는 방송)으로 인한 혼잡을 피하도록 한다. 그러나 《신호통보》라고 부르는 통보문은 목적주소가 미리 정의되여있지 않다.이 신호통보는 통신요구가 “one to many”인 경우에 리용하므로 《선택》기구에서 동작하도록 설계한다.

모선통신을 진행할 때 프로그람에는 봉사이름(Service Names)이 필요하다. 이 봉사이름은 같은 모선에서 다른 프로그람으로 리용할수 있다. 봉사이름은 D-Bus daemon에 의해 중계되는데 통보를 어떤 프로그람에서 다른 프로그람에로 발송하는데 리용된다. 봉사이름의 개념은 IP주소와 주콤퓨터이름의 개념과 비슷하다. 일반적으로 콤퓨터는 하나의 IP주소와 망봉사종류에 따르는 여러개의 주콤퓨터이름을 가질수 있다. 만일 모선을 리용하지 않으면 봉사이름이 필요없다.

실지 응용에서는 일반적으로 봉사를 정의하는 조직의 령역이름으로 봉사이름을 정한다.

례를 들어 D-Bus봉사는 freedesktop.org가 정의하므로 모선에서 “org.freedesktop. DBus”봉사이름으로 찾을수 있다.

망의 주콤퓨터에서와 같이 프로그람은 객체를 반출하여 다른 프로그람들에 특정한 봉사를 제공한다. 이 객체들은 층구조와 부모자식관계가 거의 비슷한데 모두 QObject에서 파생된다. 한가지 다른 점은 《뿌리객체》의 개념을 가진다는것이다. 즉 모든 객체들은 하나의 최종적인 부모가 있다는것이다.

객체경로(object path)는 Web봉사의 URL경로부분과 같다. D-Bus에서 객체경로는 화일체계에서의 경로이름과 비슷한데 “/”으로 분리된 꼬리표이다. 매 꼬리표는 자모, 수자, 밑선으로 이루어져있다. 경로는 반드시 “/”기호로 시작되여야 한다. 그러나 “/”기호로 끝나지 않아도 된다.

#### 2) 대면부와 접속기

거의 모든 분산프로그람들과 같이 D-Bus에 기초한 프로그람에는 일반적으로 의뢰기프로그람과 봉사기프로그람이 있다. 봉사를 제공하는 객체는 접속기(adaptor)로 D-Bus에 방문대면부를 출력한다. 의뢰기는 이 표준대면부를 리용하여 이 객체를 찾은 다음 봉사객체의 련관기능을 리용한다. 대면부는 원격봉사객체가 의뢰기프로그람에 제공하는 방문대리이다. 의뢰기프로그람은 대면부를 리용하여 원격객체의 메쏘드와 원격객체를 련결하는 신호를 호출할수 있으며 get/set방법을 리용하여 원격객체속성을 읽기, 쓰기할수 있다.

QtDBus모듈에서 대면부는 QDBusAbstractInterface기초클라스를 가지고있다. 모든 대면부들은 다 이 클라스로부터 계승되여 창조된다. 그러므로 수동으로 편집하지 않아도 된다. 이 방법을 일반적으로 정적호출이라고 한다.

QtDBus모듈은 원격객체방문포구 QDBusInterface를 제공하는데 정적으로 창조한 대면부가 없을 때 동적인 원격객체방문방식을 제공한다.

례를 들어 D-Bus에서 봉사이름이 com.example.Calculator, 객체경로가 com.example. Calculator, 대면부이름이 org.mathematics.RPNCalculator인 객체를 호출하여 간단한 제곱(210)계산을 진행하는 프로그람은 다음과 같다.

QDBusInterface remoteApp(“com.example.Calculator”, “/Calculator/Operations”, “org.mathematics.RPNCalculator”);

remoteApp.call(“Push”, 2);

remoteApp.call(“Push”, 2);

remoteApp.call(“Execute”, “^”);

QDBusReply<int> reply=remoteApp.call(“Pop”);

if (reply.isValid())

printf(“%d”, reply.value());

여기서 의뢰기는 QDBusInterface대면부의 call()함수를 호출하여 원격객체의 Push()함수, Execute()함수, Pop()함수를 순서대로 방문하고 마지막에 결과를 출력한다.

QtDBus모듈에는 또한 실용대면부클라스 QDBusConnectionInterface가 있는데 이것은 D-Bus daemon프로쎄스가 제공하는 봉사(례를 들어 현재 모선에 련결되여있는 리용자목록정보 등을 방문하는것과 같은 봉사)를 방문하는데 리용한다.

QtDBus모듈의 접속기는 특수한 클라스이다. 이것은 임의의 QObject에서 계승되는 객체에 붙어있을수 있으며 이 객체의 방문대면부로 D-Bus의 외부체계를 리용한다. 접속기클라스에는 실체객체사이에 호출을 넘겨주어 검증을 하거나 외부입력형식을 전환하여 실체객체를 보호하는 기능이 있다. 다중계승과 다른것은 접속기를 리용하면 임의의 시각에 객체를 추가할수 있으며 현재 개체를 출력할 때 더 높은 유연성을 가진다는것이다. 접속기는 또한 서로 다른 대면부에서 같은 이름으로 그와 비슷한 기능(례를 들어 어떤 객체에 새 판본의 대면부를 추가하는 기능)을 제공할수 있다.

자체정의한 접속기클라스는 반드시 QDBusAbstractAdaptor클라스에서 계승되여야 한다. 접속기클라스는 이 클라스가 QObject의 자식클라스이기때문에 Q_OBJECT마크로를 반드시 선언해주어 moc도구가 원천화일을 처리할수 있게 한다. 접속기클라스는 또한 최소한 하나의 “D-Bus Interface”로 이름지어지는 Q_CLASSINF()항목을 이 선언을 출력하는 대면부로 설정한다.

각종 호출형태의 통보들은 모선을 리용하여 접속기클라스의 공개처리부함수를 방문할수 있다. 접속기클라스에서도 신호들은 자동적으로 D-Bus에서 련속 전달된다.

또한 Q_PROPERTY로 선언한 속성은 D-Bus의 속성대면부에 자동적으로 보내진다. 그러나 Q_Object의 속성체계에서는 읽기불가능한 속성이 존재하지 못하게 한다. 그러므로 접속기클라스에서는 오직 쓰기속성만을 선언할수 없다.

QDBusAbstractAdaptor클라스는 모든 D-Bus접속기들의 기초클라스이다. 또한 모든 객체들은 D-Bus에서 외부로 출력하는 표준대면부의 시작점으로 된다.

D-Bus에서 객체를 외부로 출력하는 순서는 다음과 같다.

① QDBusAbstractAdaptor에서 계승한 접속기를 얻는다.

② 이 접속기를 출력객체에 붙인다.(이 객체는 반드시 QObject로부터 계승되여야 한다.)

③ QDBusConnection::registerObject()함수를 호출하여 이 출력객체를 등록한다.

D-Bus가 전송하는 통보의 류형은 Qt에서 직접 리용할수 없다. 그러므로 QtDBus모듈은 Qt에서 일부 자료류형들을 수정하여 리용한다.

QtDBus모듈에서 리용자가 자기의 자료류형을 정의하려면 Q_DECLARE_META TYPE()마크로로 선언을 한 다음 qDBusRegisterMetaType()함수로 등록을 하여야 한다.

## 제3절. 다매체처리

### 1. 화상처리

#### 1) QPixmap

화상을 처리하기 위한 클라스에는 주요하게 QPixmap와 QImage가 있다.

QPixmap클라스는 화상의 그리기에 리용되며 QImage클라스는 화상의 입출력과 화소에 대한 직접적인 접속 및 처리에 리용된다.

Pixmap는 조작체계에 의하여 내적으로 관리되는 화소에 기초한 그리기장치에 그려진 화상이다. Pixmap는 화면이나 인쇄기와 같은 출구장치에 그려진 화상이 아니라 기억기에 그려진 화상이다.

Pixmap를 리용하는 목적은 창문부분품을 갱신할 때라든가 복잡한 그리기가 진행될 때 떠는 현상이 없도록 하자는데 있다. Pixmap를 그리고 그것을 창문부분품에 단번에 표시하면 떠는 현상을 없앨수 있다.

Pixmap의 화소자료는 내적으로 보관되고 조작체계에 의하여 관리되므로 화소들에 직접 접속할수 없으며 bitBlt()함수나 QPainter클라스의 함수들, QImage로 변환하여서만 화소들을 조작할수 있다.

그러나 창문부분품과 관련된 클라스들에는 Pixmap화상자료를 쉽게 표시할수 있게 하여주는 setPixmap()함수들이 제공되여있다. 례를 들어 QLabel::setPixmap()함수를 리용하여 화면에 Pixmap화상을 표시할수 있고 QButton::setPixmap()함수로 단추에도 Pixmap화상을 쉽게 표시할수 있다.

Pixmap를 리용하여 창문부분품을 유연하게 갱신하는 일반적인 단계는 다음과 같다.

① 창문부분품과 꼭같은 크기의 Pixmap를 창조한다.

② Pixmap를 창문부분품의 배경색으로 채운다.

③ Pixmap에 그리기한다.

④ 창문부분품안에 Pixmap의 내용을 bitBlt()함수로 표시한다.

QPixmap클라스의 width(), height(), size()함수를 리용하여 Pixmap의 폭과 높이, 크기를 얻을수 있고 resize()함수로 크기를 변화시킬수 있으며 rect()함수를 통하여 Pixmap에 대한 4각형도 쉽게 얻는다.

또한 depth()함수로 Pixmap의 깊이를 얻을수 있다. 여기서 Pixmap의 깊이란 Pixmap의 화소당 비트수(bpp) 또는 비트평면수를 말한다. 화상의 깊이도 마찬가지다.

fill()함수로 어떤 색갈 또는 어떤 창문부분품의 배경색이나 배경화상으로 Pixmap를 채울수 있다.

createHeuristicMask()함수로써 Pixmap로부터 마스크를 창조할수 있으며 setMask()함수로써 마스크를 설정하고 mask()함수로 설정된 Pixmap의 마스크를 얻을수 있다.

load()함수로써 화일로부터 Pixmap를 적재할수 있고 loadFromData()함수로 어떤 두값자료로부터 Pixmap를 적재할수도 있다.

convertToImage()함수와 convertFromImage()함수를 리용하여 Pixmap와 화상사이의 호상변환을 진행할수 있다.

bitBlt()함수는 한 그리기장치의 화상을 다른 그리기장치에로 지정한 라스터연산코드를 리용하여 복사한다. 이 함수는 QPixmap의 성원함수가 아니라 Qt의 대역함수이다.

void bitBlt(QPaintDevice *dst, int dx, int dy, const QPaintDevice *src, int sx, int sy, int sw, int sh, Qt::RasterOp=CopyROP rop, bool ignoreMask=FALSE)

void bitBlt(QPaintDevice *dst, constQPoint &dp, const QPaintDevice

*src, const QRect &sr, RasterOp rop=CopyROP)

여기서 src는 원천그리기장치, dst는 목적그리기장치, sx와 sy는 원천화상의 왼쪽웃구석자리표, sw, sh는 원천화상의 폭과 높이, sr는 원천화상에 대한 4각형, dx와 dy는 목적화상의 왼쪽웃구석자리표, dp는 목적화상의 왼쪽웃구석점, rop는 라스터연산코드, ignore Mask는 마스크화하겠는가 안하겠는가를 지정한다.

아래에 Pixmap에 그린 화상을 창문부분품에 표시하는 실례를 준다.

void CuteWidget::paintEvent(QPaintEvent *e)

{

QRect ur=e→rect(); //갱신할 4각형얻기

QPixmap pix(ur.size()); //Pixmap창조

pix.fill(this,ur.topLeft()); //창문부분품의 배경으로 Pixmap채우기

QPainter p(&pix);

p.translate(-ur.x(),-ur.y())//창문부분품의 자리표로 Pixmap에 그리기 위하여

//…Pixmap에 그리기진행…

p.end();

bitBlt(this,ur.topLeft(),&pix);

}

QPixmap클라스로부터 파생된 QBitmap클라스는 흑백색 Pixmap만을 지원한다.

#### 2) QImage

QImage클라스는 1-bpp, 8-bpp,32-bpp화상자료를 지원하며 1-bpp, 8-bpp화상자료들은 색표를 리용하며 화소값은 색표의 첨수이다. 32-bpp화상은 색표를 리용하지 않으며 아래자리 3바이트는 RGB값을, 제일웃자리바이트는 알파완충기로 리용된다.

알파완충기란 화소의 투명도를 결정하는 바이트로서 0이면 완전한 투명을 의미하고 255이면 완전한 불투명을 의미한다. 알파완충기는 마스크화상을 창조하는데 리용된다.

알파완충기가 작용하게 하겠는가 작용하지 못하게 하겠는가를 지정하는것을 알파완충기방식이라고 하며 알파완충기방식은 setAlphaBuffer()함수에 TRUE나 FALSE를 넘겨 설정하거나 설정하지 않으며 알파완충기방식이 설정되였는가는 hasAlphaBuffer()함수로써 알수 있다.

알파완충기방식이 설정되였을 때 createAlphaMask()함수는 알파완충기로부터 마스크화상을 QBitmap객체로 얻어낸다.

알파완충기방식이 설정되지 않은 경우에는 createHeuristicMask()함수로 마스크화상을 창조할수 있는데 이 함수는 화상의 어떤 한 구석점으로부터 색을 선택하고 모든 가장자리로부터 시작하여 그 색갈의 화소들만을 떼여내는 방법으로 마스크화상을 창조한다.

colorTable()함수를 리용하여 색표에 대한 지적자를 얻을수 있으며 numColors()함수로 색표의 크기 즉 색갈개수를 얻을수 있고 setNumColors()함수로 색표의 크기를 재설정할수 있다.

setColor()함수를 리용하여 색표안에서 지정한 첨수에 대한 색을 어떤 색으로 설정할수 있고 color()함수로 색표안에서 지정한 첨수에 대한 색을 얻을수 있다.

scanLine()함수는 지정한 첨수를 가진 주사행(첫 주사행의 첨수는 0)에 대한 화소자료들에 대한 지적자를 uchar*형으로 얻는다. 이때 얻어진 지적자는 비트순서에 의존하므로 직접 리용할수 없으며 QRgb*형으로 형변환하여야 개별적인 화소값들을 읽기쓰기할수 있다. 얻어진 RGB색에서 매 요소색들을 따내려면 qRed(), qGreen(), qBlue()대역함수들을 리용하면 된다.

bits()함수는 첫 화소자료에 대한 지적자를 uchar*형으로 얻으며 이것은 scanLine(0)과 동등하다. numBytes()함수는 화상자료의 총 바이트크기를 얻으며 bytesPerLine()함수는 한개 주사행에 대한 바이트크기를 얻는다.

scale()함수는 지정한 폭 w와 높이 h 또는 크기 s(단위는 모두 화소수)를 가진 4각형안에 지정한 확대축소방식 mode에 따라 들어차도록 확대축소된 화상을 돌려준다.

확대축소방식에는 3가지가 있는데 ScaleFree이면 지정한 4각형안에 꽉 들어차도록 확대 또는 축소하며 ScaleMin이면 화상의 폭과 높이의 비는 보존하면서 지정한 4각형안에 가능한껏 들어차도록 확대 또는 축소하며 ScaleMax이면 화상의 폭과 높이의 비를 보존하면서 지정한 4각형안에 꽉 들어차고 가능한껏 적게 벗어나도록 확대 또는 축소한다.

scale()함수는 화상을 확대축소하는 속도는 빠르지만 화상의 질은 높지 못하며 화상의 질을 높이려면 smoothScale()함수를 리용하면 된다.

scaleWidth()와 scaleHeight()함수는 폭 또는 높이만 지정하여 확대축소하며 이때 화상의 폭과 높이의 비는 보존된다. fill()함수는 지정한 값으로 모든 화소들을 채우며 이때 알파완충기는 변화시키지 않는다.

pixel()함수는 지정한 자리표에 있는 화소의 색을 돌려주며 setPixel()함수는 지정한 자리표에 있는 화소의 색을 지정한 색(또는 첨수)으로 설정한다.

pixelIndex()함수는 지정한 자리표에 있는 화소의 첨수를 돌려준다.

invertPixels()함수는 모든 화소값들을 반전하며 이때 파라메터로 TRUE를 지정하면 알파완충기도 반전한다.

valid()함수는 지정한 자리표에 있는 점이 화상안의 점이면 TRUE 아니면 FALSE를 돌려준다.

swapRGB()함수는 RGB화상으로부터 BGR화상을 돌려주며 mirror()함수는 수직 또는 수평방향으로의 거울반사효과로서 얻어진 화상을 돌려준다.

setOffset()함수는 다른 화상에 관한 상대위치를 지정하기 위한 X축과 Y축방향의 편위값에 대한 화소수들을 설정하며 offset()함수는 setOffset()함수에 의하여 설정한 값을 얻는다.

dotsPerMeterX()와 dotsPerMeterY()함수는 1m길이에 들어있는 화소수를 돌려주며 setDotsPerMeterX()와 setDotsPerMeterY()함수는 1m길이에 들어있는 화소수를 설정하며 이것들은 화상의 확대축소와 관련된다.

배경이 투명한 화상만을 화면에 표시하여보자. 그리고 화상을 마우스로 찰칵한 상태에서 화면의 임의의 위치에 옮길수 있게 하자.

void MoveMe::mousePressEvent(QMouseEvent*e){clickPos=e→pos();}

void MoveMe::mouseMoveEvent(QMouseEvent*e){move(e→globalPos()-clickPos);}

int main(int argc, char **argv) {

QApplication a(argc, argv);

QString fn="tux.png";

if (argc >= 2)

fn = argv[1];

if (!QFile::exists(fn))

exit(1);

QImage img(fn);

QPixmap p;

p.convertFromImage(img);

if(!p.mask())//마스크화상이 설정되여있지 않으면

if (img.hasAlphaBuffer())//알파완충기가 유효하면

{

QBitmap bm;

bm =img.createAlphaMask();

p.setMask(bm);

}

else //알파완충기가 유효하지 않으면

{

QBitmap bm;

bm=img.createHeuristicMask();

p.setMask(bm);

}

MoveMe w(0,0,Qt::WStyle_Customize|Qt::WStyle_NoBorder);

//창문의 제목띠와 경계들을 없앤다.

w.setBackgroundPixmap(p); //창문의 배경을 Pixmap로 설정

w.setFixedSize(p.size()); //창문의 크기를 화상의 크기로 고정

if (p.mask())

w.setMask(*p.mask()); //창문을 Pixmap의 마스크화상으로 마스크하여 투명하게 한다.

w.show();

a.setMainWidget(&w);

return a.exec();

}

#### 3) QPicture클라스

QPicture클라스는 QPainter클라스의 지령(함수호출)들을 기록하였다가 재현할수 있는 그리기장치를 제공하며 이러한 그리기장치를 picture라고 한다.

Windows에서는 메타화일과 류사하다고 볼수 있지만 Qt에서는 그 내용에서 특별한 제한이 없다. 즉 서체, Pixmap, 령역, 변화된 도형이나 화상 등 QPainter클라스의 지령들로 그릴수 있는 모든것이 다 QPicture객체에 기록할수 있다.

QPainter객체에 그리기한 내용을 QPicture객체에 기록하려면 다음의 단계들을 거쳐야 한다.

① QPicture객체와 QPainter객체를 창조하여야 한다.

② QPainter객체의 begin()함수를 QPicture객체를 파라메터로 넘겨 호출하여야 한다.

그래야 QPainter객체의 그리기함수들을 호출하면 QPicture객체에 그리기된다.

③ QPainter객체의 그리기함수들을 호출하여 그리기를 진행한다.

④ QPainter객체의 end()함수를 호출하여 그리기를 끝낸다.

⑤ QPicture객체의 save()함수를 보관하려는 화일이름을 파라메터로 넘겨 호출하여야 한다. picture화일의 확장자는 “.pic”이다.

아래의것은 picture에 기록하는 간단한 실례이다.

QPicture pic;

QPainter p;

p.begin(&pic);

p.drawEllipse(10,20,80,70);

p.end();

pic.save("drawing.pic");

QPicture객체에 기록한 내용을 재현하려면 다음의 단계들을 거쳐야 한다.

① QPicture객체를 창조한다.

② QPicture객체의 load()함수를 pictu화일의 경로를 파라메터로 넘겨 호출하여야 한다.

③ QPainter객체를 창조하고 QPainter객체의 begin()함수를 그리기하려는 창문을 파라메터로 넘겨 호출하여야 한다.

④ QPainter객체의 그리기함수들을 호출하여 그리기를 진행한다.

⑤ QPainter객체의 end()함수를 호출하여 그리기를 끝낸다.

아래의것은 picture에 기록한 내용을 재현하는 실례이다.

QPicture pic;

pic.load("drawing.pic");

QPainter p;

p.begin(&myWidget);

p.drawPicture(pic);

p.end();

QPicture객체의 play()함수를 QPainter객체를 파라메터로 넘겨 호출하여도 picture에 기록한 내용을 재현할수 있다.

setData()함수를 리용하여 지정한 크기의 지정한 자료를 직접 picture자료로 설정할수도 있으며 data()함수에 의하여 picture자료를 얻을수 있다.

size()함수는 picture자료의 크기를 얻으며 isNull()함수는 picture자료가 비였는가 비지 않았는가를 돌려준다. setBoundingRect()와 boundingRect()함수는 picture의 경계4각형을 설정하거나 얻는다.

#### 4) XPM, XBM화상격식

XPM화상격식은 화상자료를 본문형식으로 보관하기 위한 격식이다. 그러므로 XPM화상격식은 본문편집기를 리용하여 창조하고 수정할수 있으며 XPM화일의 내용은 프로그람원천코드에 그대로 복사하여 그 XPM화일의 화상을 표시할수 있게 하여준다.

XPM화상격식의 화일의 실례는 다음과 같다.

/*XPM*/

static const char *essPixmap[]={

“12 14 4 1”,

“ c None”,

“X c #FFFFFF”,

“R c Red”,

“B c #0000FF”,

“ RRBB “,

“XXXXXXXXXXXX”,

“XXXXXXXXXXXX”,

“XX RRBB ”,

“XX RRBB ”,

“XX RRBB ”,

“XXXXXXXXXXXX”,

“XXXXXXXXXXXX”,

“ RRBB XX”,

“ RRBB XX”,

“ RRBB XX”,

“XXXXXXXXXXXX”,

“XXXXXXXXXXXX”,

“RRBB”,

};

우에서 보는것처럼 XPM화일은 본문화일이며 원천코드이다.

첫번째 행의 설명문 “/*XPM*/”은 XPM화일이라는것을 나타낸다. 두번째 행의 문자렬배렬변수이름은 XPM화상의 식별자이며 이 변수가 가지는 문자렬들이 화상자료로 된다.

문자렬배렬의 첫 문자렬에는 공백으로 구분된 4 개의 수값을 지정하여야 하는데 그것들은 차례로 화상의 폭, 높이, 리용하려는 색갈개수, 하나의 색을 표현하는데 리용하려는 문자개수이다. XPM화상격식에서는 색을 표현하는데 ASCII문자들을 리용하며 매 색을 표현하는데 리용되는 문자들을 태그라고 한다.

문자렬배렬의 두번째 문자렬부터는 “c”로 구분한 태그와 대응되는 색을 지정하며 이러한 문자렬의 개수는 색을 표현하는데 리용하려는 색개수와 같아야 한다. 색은 #기호로 시작한 16진수로 지정할수도 있고 Qt에서 미리 정의된 색상수(Red, Green 등)로 지정하여도 되며 투명을 지정하려면 None을 지정한다.

문자렬배렬의 다음 문자렬부터는 화상의 색자료들을 지정하여야 하는데 화상의 높이만한 개수의 문자렬들을 지정하여야 한다. 매 문자렬들은 태그들로 이루어지며 화상의 폭에 태그의 문자수를 곱한 값만한 개수의 문자들을 지정하여야 한다. 매 태그는 해당한 화소의 색을 나타낸다.

XBM화상격식도 본문형식으로 보관되며 XPM화상격식과 다른것은 흑백색화상만을 제공한다는것이다. 그러므로 화상의 매 화소는 하나의 비트로 표현되며 이 비트들의 렬을 단순히 지정하면 XBM화상이 생성된다.

다음의 실례는 아래의 그림과 같은 화상을 표시하는 XBM화상이다.

static unsigned char arrow_bits[]=

{0x00,0x00,0x00,0x00,0xc0,0x07,0x80,0x0f,0x80,0x1f,0xfc,0x3f,0xfc,0x7f,0xfc,0xff,0xfc,0x7f,0xfc,0x3f,0x80,0x1f,0x80,0x0f,0xc0,0x07,0x00,0x00,0x00,0x00,0x00,0x00};

### 2. 음성처리

이 실례는 WAV형식의 화일로부터 파형자료를 추출하여 그라프로 표시하는 방법을 프로그람으로 실현한다.

#include "waveview.h"

#include <qvariant.h>

#include <qscrollbar.h>

#include <qlayout.h>

#include <Qtooltip.h>

#include <qwhatsthis.h>

#include <qpainter.h>

#include <qfile.h>

WaveViewer::WaveViewer(QWidget* parent, const char* name, WFlags fl)

: QWidget(parent, name, fl) {

if (!name)

setName("WaveViewer");

scrlHorz=newQScrollBar(this, "scrlHorz");

scrlHorz→setGeometry(QRect(10,370, 551, 21));

scrlHorz→setOrientationQScrollBar::Horizontal);

scrlHorz→setRange (0, 1000);

scrlHorz→setSteps (1, 100);

scrlVert=new QScrollBar(this, "scrlVert");

scrlVert→setGeometry(QRect(560, 10, 21, 350));

scrlVert→setOrientation(QScrollBar::Vertical);

scrlVert→setRange (1, 100);

scrlVert→setSteps (1, 10);

languageChange();

resize(QSize(600, 400).expandedTo(minimumSizeHint()));

clearWState(WState_Polished);

m_pWave=NULL;

connect(scrlHorz, SIGNAL(valueChanged(int)), this, SLOT(changeHorzScroll(int)));

connect(scrlVert, SIGNAL(valueChanged(int)), this, SLOT(changeVertScroll(int)));

}

WaveViewer::~WaveViewer(){

if (m_pWave!=NULL)

free(m_pWave);

}

void WaveViewer::languageChange() { setCaption(tr("wave view")); }

void WaveViewer::changeHorzScroll(int nVal) { repaint(); }

void WaveViewer::changeVertScroll(int nVal) { repaint(); }

void WaveViewer::resize(int w, int h) {

w-=20; h-=40;

crlHorz→setGeometry(QRect(0, h+20, w, 20));

scrlHorz→setSteps(1, w);

scrlVert→setGeometry(QRect(w, 20, 20, h));

}

void WaveViewer::resize(QSize size) {

int w, h;

w=size.width();

h=size.height();

resize(w, h);

}

void WaveViewer::paintEvent(QPaintEvent *e) {

int nW, nH;

int nCY;

long nOfst;

QPainter p(this);

nW=width()-20;

nH=height()/2-20;

nCY=20+nH;

p.drawLine (0, nCY, nW, nCY);

if (m_pWave==NULL)

return;

outWaveInfo(&p);

nOfst=scrlHorz→value()*100;

drawOrgWave(&p, nOfst, nCY, nW, nH);

}

void WaveViewer::outWaveInfo(QPainter *painter) {

WAVEINFOHEADER *pInfo;

char szBuff [128];

pInfo= (WAVEINFOHEADER*)(m_pWave+12);

printf (szBuff, "SamplesPerSec=%d, Channels=%d, BitsPerSample=%d",

pInfo→nSamplesPerSec, pInfo→nChannels, pInfo→nBitsPerSample);

painter→drawText(0,16, tr(szBuff));

}

void WaveViewer::drawOrgWave(QPainter *painter, long nOfst, int nCY, int nW, int nH) {

short *pBits;

long nSize, nSamples;

nScale, nChannels;

int nI, nJ, nK;

int nX1, nY1, nX2, nY2;

double dfVal;

pBits= (short*)waveBits();

nSize= (long)waveSize();

nChannels=waveChannels();

nScale=scrlVert→value();

QPen penOld;

QPen penBlue (QColor (0, 0, 255), 1, QPen::SolidLine);

penOld=painter→pen ();

painter→setPen (penBlue);

nSamples=nSize/nChannels;

for (nI=0; nI<nW; nI++) {

nJ=nOfst+nI;

if (nJ>=nSamples)

continue;

dfVal= (double)(pBits [nJ *nChannels] -m_nY0) / (double)m_nMax;

dfVal*= (double)nScale;

if (dfVal>1.0)

dfVal=1.0;

if (dfVal<-1.0)

dfVal=-1.0;

dfVal*= (double)nH; if (dfVal<0.0)

nK= (int)(dfVal-0.5);

else

nK= (int)(dfVal+0.5);

if (nI==0) {

nX1=nI;

nY1=nCY+nK;

continue;

}

nX2=nI;

nY2=nCY+nK;

painter→drawLine (nX1, nY1, nX2, nY2);

nX1=nX2;

nY1=nY2;

}

painter→setPen(penOld);

}

bool WaveViewer::loadWave(const QString& fileName) {

QFile file(fileName);

if (!file.open(IO_ReadOnly))

return FALSE;

RIFFHEADER riffHeader;

unsigned long dwBitsSize;

int nSize, nSamples;

dwBitsSize=file.size();

nSize=sizeof(RIFFHEADER);

if (file.readBlock((char*)&riffHeader, nSize)!= nSize)

returnFALSE;

if (strncmp(riffHeader.cMark, "RIFF", 4))

return FALSE;

dwBitsSize-=nSize;

m_pWave= (char*)malloc(dwBitsSize);

if (m_pWave==NULL)

return FALSE;

if (file.readBlock (m_pWave, dwBitsSize)!= dwBitsSize){

free(m_pWave);

m_pWave=NULL;

return FALSE;

}

setLevels();

nSamples=waveSize()/waveChannels();

scrlHorz→setRange (0, nSamples/100);

scrlHorz→setSteps (1, 10);

scrlHorz→setValue (0);

return TRUE;

}

bool WaveViewer::saveWave(const QString& fileName) { return TRUE; }

short WaveViewer::waveChannels() {

WAVEINFOHEADER *pInfo;

pInfo=(WAVEINFOHEADER *)(m_pWave+12);

return (short)pInfo→nChannels;

}

unsigned long WaveViewer::waveSize() {

WAVEINFOHEADER *pInfo;

unsigned long dwSize, *pData;

pInfo= (WAVEINFOHEADER *)(m_pWave+12);

pData= (unsignedlong*)(pInfo+1);

dwSize=pData [1] / (pInfo→nBitsPerSample/8);

return dwSize;

}

char *WaveViewer::waveBits() {

WAVEINFOHEADER *pInfo;

unsigned long *pData;

char *pBits;

pInfo = (WAVEINFOHEADER *)(m_pWave+12);

pData= (unsigned long *)(pInfo+1);

pBits= (char*)(pData+2);

return pBits;

}

void WaveViewer::setLevels() {

long *pCount;

short *pBits;

long lIndex, lSize, lPos, lVal;

pBits= (short *)waveBits ();

//령준위를 추출한다.

pCount=new long [70000];

for (lIndex=0; lIndex<70000; lIndex++)

pCount[lIndex]=0;

lSize=waveSize();

for (lIndex=0; lIndex<lSize; lIndex++){

lVal= (long)pBits [lIndex] +35000;

pCount[lVal] ++;

}

lPos=0;

for (lIndex=0; lIndex<70000; lIndex++){

if (pCount[lPos] <pCount[lIndex])

lPos=lIndex;

}

m_nY0= (short)(lPos-35000);

delete[] pCount;

//최대 진폭을 추출한다.

m_nMax=0;

for (lIndex=0; lIndex<lSize; lIndex++)

{

lVal=abs (pBits[lIndex] - m_nY0);

if (m_nMax<lVal)

m_nMax=lVal;

}

}

Test클라스에서 ImageViewer창문부분품을 중심령역으로 설정한다.

Test::Test(): QMainWindow(0, "Test", WDestructiveClose) {

…………………………………

v=new WaveViewer (this, "MyWidget");

v→setFocus();

setCentralWidget(v);

resize(600, 300);

m_nGapH=menuBar()→heightForWidth(600);

m_nGapH+=statusBar()→height();

QDockArea *dock=topDock();

if (dock!= NULL)

m_nGapH+=dock→height();

m_nGapH-=10;

v→resize (600, 300-m_nGapH);

…………………………………

}

void Test::load(const QString &fileName) { v→loadWave(fileName); }

Test::Test(): QMainWindow(0, "Test", WDestructiveClose) {

…………………………………

v=new WaveViewer (this, "MyWidget");

v→setFocus();

setCentralWidget(v);

resize(600, 300);

m_nGapHmenuBar()→heightForWidth(600);

m_nGapH+=statusBar()→height();

QDockArea *dock=topDock ();

if (dock!= NULL)

m_nGapH+=dock→height ();

m_nGapH-=10;

v→resize(600, 300-m_nGapH);

…………………………………

}

void Test::load(const QString &fileName) {

v→loadWave(fileName);

v→repaint();

setCaption(filename);

statusBar()→message(trUtf8("%1문서가 적재되였습니다.") .arg(fileName), 2000);

}

void Test::save() {

if (filename.isEmpty()){

saveAs();

return;

}

if (!v→saveWave (filename)) {

statusBar()→message(trUtf8("%1화일로 쓸수 없습니다.") .arg(filename), 2000);

return;

}

statusBar()→message(trUtf8("%1화일로 보관되였습니다.") .arg(filename), 2000);

}

### 3. 동화상재생

Movies실례는 MNG와 동화상 GIF화일들을 QMovie와 QLabel클라스들을 사용하여 보여준다.

#include <qapplication.h>

#include <qfiledialog.h>

#include <qpushbutton.h>

#include <qlabel.h>

#include <qpainter.h>

#include <qmessagebox.h>

#include <qmovie.h>

#include <qvbox.h>

class MovieScreen : public QFrame {

Q_OBJECT

QMovie movie;

QString filename;

QSize sh;

public:

MovieScreen(const char* fname, QMovie m, QWidget* p=0, const char* name=0,WFlags f=0) : QFrame(p, name, f), sh(100, 100)

{

setCaption(fname);

filename = fname;

movie = m;

setFrameStyle(QFrame::WinPanel|QFrame::Sunken);

movie.setBackgroundColor(backgroundColor());

setBackgroundMode(NoBackground);

movie.connectUpdate(this, SLOT(movieUpdated(const QRect&)));

movie.connectResize(this, SLOT(movieResized(const QSize&)));

movie.connectStatus(this, SLOT(movieStatus(int)));

setSizePolicy(QSizePolicy(QSizePolicy::Expanding,QSizePolicy::Expanding));

}

QSize sizeHint() const { return sh; }

protected:

void drawContents(QPainter* p) {

QPixmap pm = movie.framePixmap();

QRect r = contentsRect();

if (!pm.isNull()) {

if (r.size() != pm.size()) {

QWMatrix m;

m.scale((double)r.width()/pm.width(), (double)r.height()/pm.height());

pm = pm.xForm(m);

}

p→drawPixmap(r.x(), r.y(), pm);

}

const char* message = 0;

if (movie.paused()) {

message = "PAUSED";

} else if (movie.finished()) {

message = "THE END";

} else if (movie.steps() > 0) {

message = "FF >>";

}

if (message) {

p→setFont(QFont("Helvetica", 24));

QFontMetrics fm = p→fontMetrics();

if (fm.width(message) > r.width()-10)

p→setFont(QFont("Helvetica", 18));

fm = p→fontMetrics();

if (fm.width(message) > r.width()-10)

p→setFont(QFont("Helvetica", 14));

fm = p→fontMetrics();

if (fm.width(message) > r.width()-10)

p→setFont(QFont("Helvetica", 12));

fm = p→fontMetrics();

if (fm.width(message) > r.width()-10)

p→setFont(QFont("Helvetica", 10));

p→setPen(black);

p→drawText(1, 1, width()-1, height()-1, AlignCenter, message);

p→setPen(white);

p→drawText(0, 0, width()-1, height()-1, AlignCenter, message);

}

}

public slots:

void restart() {

movie.restart();

repaint();

}

void togglePause() {

if (movie.paused())

movie.unpause();

else

movie.pause();

repaint();

}

void step() {

movie.step(); repaint();

}

void step10() {

movie.step(10); repaint();

}

private slots:

void movieUpdated(const QRect& area) {

if (!isVisible())

show();

QRect r = contentsRect();

if (r.size() != movie.framePixmap().size()) {

repaint(r);

} else {

repaint(area.x()+r.x(), area.y()+r.x(), area.width(), area.height());

}

}

void movieResized(const QSize& size) {

int fw = frameWidth();

sh = QSize(size.width() + fw*2, size.height() + fw*2);

updateGeometry();

if (parentWidget() && parentWidget()→isHidden())

parentWidget()→show();

}

void movieStatus(int status) {

if (status < 0) {

QString msg;

msg.sprintf("Could not play movie \"%s\"", (const char*)filename);

QMessageBox::warning(this, "movies", msg);

parentWidget()→close();

} else if (status == QMovie::Paused || status == QMovie::EndOfMovie) {

repaint();

}

}

};

class MoviePlayer : public QVBox {

MovieScreen* movie;

public:

MoviePlayer(const char* fname, QMovie m, QWidget* p=0, const char* name=0,WFlags f=0) : QVBox(p, name, f) {

movie = new MovieScreen(fname, m, this);

QHBox* hb = new QHBox(this);

QPushButton* btn;

btn = new QPushButton("<<", hb);

connect(btn, SIGNAL(clicked()), movie, SLOT(restart()));

btn = new QPushButton("||", hb);

connect(btn, SIGNAL(clicked()), movie, SLOT(togglePause()));

btn = new QPushButton(">|", hb);

connect(btn, SIGNAL(clicked()), movie, SLOT(step()));

btn = new QPushButton(">>|", hb);

connect(btn, SIGNAL(clicked()), movie, SLOT(step10()));

}

};

MovieStarter::MovieStarter(const char *dir) : QFileDialog(dir, "*.gif *.mng") {

setMode(ExistingFile);

connect(this, SIGNAL(fileSelected(const QString&)), this, SLOT(startMovie(const QString&)));

}

void MovieStarter::startMovie(const QString& filename) {

if (filename)

(new MoviePlayer(filename, QMovie(filename), 0, 0, WDestructiveClose))→show();

}

void MovieStarter::done(int r) {

if (r != Accepted)

qApp→quit();

setResult(r);

}

int main(int argc, char **argv) {

QApplication a(argc, argv);

if (argc > 1) {

bool gui=TRUE;

for (int arg=1; arg<argc; arg++) {

if (QString(argv[arg]) == "-i")

gui = !gui;

else if (gui)

(void)new MoviePlayer(argv[arg], QMovie(argv[arg]), 0, 0, Qt::WDestructiveClose);

else

(void)new MovieScreen(argv[arg], QMovie(argv[arg]), 0, 0, Qt::WDestructiveClose);

}

QObject::connect(qApp, SIGNAL(lastWindowClosed()), qApp, SLOT(quit()));

} else {

MovieStarter* fd = new MovieStarter(".");

fd→show();

}

return a.exec();

}

#include "main.moc"

## 제4절. 문자코드변환

### 1. Unicode

유니코드는 세계의 대다수 문서체계를 유지하는 문자부호화표준이다. 유니코드에 은페되여있는 기본원리는 문자보관에 8bit대신 16bit를 사용하여 256문자대신에 65 000개의 문자들을 부호화하는것이였다. 유니코드는 ASCII와 ISO 8859-1(Latin-1)을 같은 코드위치에서 부분모임으로 포함한다. 례를 들면 문자 'A'는 ASCII와 Latin-1, 유니코드에서 값 0x41을 가지고 문자 'b'는 Latin-1과 유니코드량쪽에서 값 0xDF을 가진다.

Qt의 QString클라스는 문자렬들을 유니코드로 보관한다. QString안의 매개 문자는 8bit char가 아니라 16bit QChar이다. 여기에 문자렬의 첫 문자를 'A'로 설정하는 2가지 방법이 있다.

str[0] = 'A';

str[0] = QChar(0x41);

원천화일이 Latin-1로 부호화되면 Latin-1문자지정은 아주 간단하다.

str[0] = 'b';

그리고 원천화일이 다른 부호화를 가지면 수값은 제대로 작업한다.

str[0] = QChar(0xDF);

임의의 유니코드문자를 그 수값으로 지정할수 있다. 례를 들면 여기에 그리스대문자 시그마('Σ')와 유로화페기호('€')를 지정하는 방법이 있다.

str[0] = QChar(0x3A3);

str[0] = QChar(0x20AC);

드문히 Latin-1이 아닌 유니코드문자들이 요구되면 문자탐색은 직결로 충분히 할수 있다.

그러나 Qt는 Qt응용프로그람에 유니코드문자렬들을 입력하는 더 편리한 수법을 제공한다.

체계에 적당한 서체들이 설치된다고 가정하면 Qt는 이러한 문서체계중의 어느것이나 사용하여 본문을 그릴수 있다. 그리고 적당한 입력방법이 설치된다고 가정하면 사용자들은 Qt응용프로그람들에서 이러한 문서체계들을 사용하는 본문을 입력할수 있다.

QChar를 사용하는 프로그람작성은 char를 사용하는 프로그람작성과 아주 다르다.

QChar의 수값을 얻으려면 그에 대하여 unicode()를 호출한다. QChar의 ASCII 혹은 Latin-1값(char)을 얻으려면 latin1()을 호출한다. Latin-1이 아닌 문자들에 대하여 latin1()은 0을 돌려준다.

프로그람안의 모든 문자렬들이 ASCII 혹은 Latin-1이라는것을 알고있으면

isalpha(), isdigit(), isspace()와 같은 표준 <cctype>함수들을 사용할수 있다. 이것들은 QString들이 자동적으로 const char *로 변환되듯이 QChars가 정확한 문맥으로 주어진 char (Latin-1)들로 자동변환되므로 제대로 작업한다. 그러나 일반적으로 이러한 조작을 수행하는데 QChar의 성원함수들을 사용하는것이 더 좋다. 그것은 QChar의 성원함수들이 임의의 유니코드문자들에 대하여 작업하기때문이다. QChar가 제공하는 함수에는 isPrint(), isPunct(), isSpace(), isMark(), isLetter(), isNumber(), isLetterOrNumber(),isDigit(), isSymbol(), lower(), upper()가 있다. 례를 들면 여기에 문자가 수자인가 대문자인가를 시험하는 방법이 있다.

if (ch.isDigit() || ch != ch.lower()) …

lower()함수는 소문자판의 문자를 돌려준다. 문자의 소문자판이 문자자체와 다르면 그 문자는 대문자이여야 한다. 코드부분은 라틴어, 그리스어를 비롯한 대소문자를 구별하는 임의의 자모에 대하여 적용된다.

QString을 요구하는 Qt의 API는 모두 유니코드문자렬을 사용할수 있다. 그때 유니코드문자렬을 적당히 현시하고 조작체계와 대화할 때 다른 부호화로 변환하는것이 Qt의 응답능력이다.

본문화일들을 읽고 쓸 때에는 특별한 주의가 필요하다. 본문화일들은 여러가지 부호화를 사용하며 그 문맥으로부터 본문화일의 부호화를 알아낼수는 없다. 기정으로 QTextStream은 읽기와 쓰기에 대하여 QTextCodec::codecForLocale()에서 유효한 체계의 국부8bit부호화를 사용한다.

자체의 화일형식을 설계하고 임의의 유니코드문자를 읽고 쓰게 하려면 QTextStream에 써넣기를 시작하기 전에 setEncoding(QTextStream::Unicode)를 호출하여 자료를 유니코드로 보관할수 있다. 그때 자료는 문자당 2byte를 요구하는 형식인 UTF-16으로 보관된다. UTF-16형식은 QString의 기억기표시와 아주 근사하므로 유니코드문자렬들을 UTF-16으로 읽고쓰는 속도는 아주 빠르다. 그러나 순수 ASCII자료를 UTF-16형식으로 보관할 때 매개 문자를 1byte대신에 2byte로 보관하므로 추가비용이 든다.

본문을 읽어들일 때 QTextStream은 보통 유니코드를 자동적으로 탐지하지만 절대적인 확신을 위하여 읽기 전에 setEncoding(QTextStream::Unicode)를 호출하는것이 제일 좋다.

유니코드전체를 유지하는 다른 부호화는 UTF-8이다. UTF16에 비한 UTF-8의 우점은 그것이 ASCII의 웃준위모임이라는것이다. 범위 0x00～0x7F의 임의의 문자는 1byte로 표시된다.

0x7F이상의 Latin-1문자들을 포함하는 다른 문자들은 여러바이트렬로 표시된다. 대체로 ASCII인 본문에서 UTF-8은 UTF-16이 소비하는 공간의 약 절반을 차지한다.

UTF-8을 QTextStream에서 사용하려면 읽고 쓰기 전에 setEncoding(QText Stream::UnicodeUTF8)를 호출해야 한다.

사용자의 지역에 관계없이 늘 Latin-1을 읽고써넣으려고 한다면 QTextStream에 대하여 setEncoding(QTextStream::Latin1)을 호출할수 있다.

적당한 QTextCodec를 리용하여 setCodec()를 호출함으로써 다른 부호화를 지정할수 있다.

QTextCodec는 유니코드와 주어진 부호화사이를 변환하는 객체이다. QTextCodec는 여러가지 문맥에서 Qt에 의해 사용된다. 내적으로 QTextCodec는 서체, 입력방식, 오려둠판, 끌어다놓기, 화일이름들을 유지하는데 쓰인다. 그러나 Qt응용프로그람을 쓸 때에도 사용할수 있다.

례를 들면 EUC-KR부호화로서 화일을 읽어들이려고 한다면 다음과 같이 쓸수 있다.

QTextStream in(&file);

QTextCodec *koreanCodec = QTextCodec::codecForName("EUC-KR");

if (koreanCodec)

in.setCodec(koreanCodec);

일부 화일형식들은 머리부에서 부호화를 지정한다. 일반적으로 머리부는 평본문 ASCII로 함으로써 어떤 부호화를 사용하는가에 관계없이 정확히 읽어들이도록 한다.(그것이 ASCII의 웃준위모임이라고 가정한다.) XML화일형식은 그러한 실례의 하나이다. XML화일들은 보통 UTF-8이나 UTF-16로 부호화된다. 그 화일들을 읽어들이는 적당한 수법은 setEncoding(QTextStream::UnicodeUTF8)을 호출하는것이다. 형식이 UTF-16이면 QTextStream는 자동적으로 이것을 탐지하고 자체로 조절한다. XML화일의 <?xml?>머리부는 흔히 부호화인수를 포함한다. 례를 들면

<?xml version="1.0" encoding="EUC-KR"?>

일단 읽기 시작하면 QTextStream이 부호화를 변경하지 못하게 하므로 명시적인 부호화를 고려하는 옳은 방법은 정확한 부호(QTextCodec::codecForName()로부터 얻어진다.)를 사용하여 그 화일을 다시 읽기 시작하는것이다.

또 하나의 QTextCodec사용은 원천코드에서 발생하는 문자렬들의 부호화를 지정하는것이다.

QTextCodec::codecForName()는 늘 유효지적자를 돌려준다. QTextCodec의 파생클라스를 만들거나 문자략도(charmap)화일을 창조하고 QTextCodec::loadCharmapFile()을 사용함으로써 다른 부호화들을 유지할수 있다.

### 2. 동적언어절환

대부분의 응용프로그람들에서는 main()에서 사용자의 언어를 탐지하여 적당한 .qm화일들을 적재하면 완전히 충족된다. 그러나 사용자들이 언어를 동적으로 절환할 필요가 있는 경우들이 있다. 여러 사람들이 번갈아 계속 사용하는 응용프로그람은 재기동하지 않고 언어를 바꿀것을 요구한다.

동적으로 언어를 절환할수 있는 응용프로그람을 만들려면 기동시에 하나의 번역을 적재하는 경우보다 좀 더 작업을 해야 하지만 어렵지 않다. 여기에 그 수행방법이 있다.

·사용자가 언어를 절환할수 있는 수단들을 제공한다.

·매개 창문부분품이나 대화창에서 번역할수 있는 문자렬들을 모두 개별적인 함수에 설정하고(흔히 retranslateStrings()를 호출하여) 언어가 달라질 때 이 함수를 호출한다.

Call Center응용프로그람의 원천코드에서 관련한 부분을 론의하자. 응용프로그람은 Language차림표를 제공하여 사용자가 언어를 실행시에 설정하게 한다. 기정언어는 영어이다.

응용프로그람이 기동할 때 사용자가 사용할 언어를 모르므로 main()함수에서 번역을 적재할 필요는 없다. 그대신에 필요할 때 번역을 동적으로 적재해야 하므로 번역을 처리하는 코드는 모두 기본창문과 대화창클라스들에 넣어야 한다.

Call Center응용프로그람의 QMainWindow파생클라스를 론의하자.

MainWindow::MainWindow(QWidget *parent, const char *name) : QMainWindow(parent, name) {

journalView = new JournalView(this);

setCentralWidget(journalView);

qmPath = qApp→applicationDirPath() + "/translations";

appTranslator = new QTranslator(this);

QtTranslator = new QTranslator(this);

qApp→installTranslator(appTranslator); qApp→installTranslator(QtTranslator);

createActions(); createMenus();

retranslateStrings();

}

구성자에서는 중심창문부분품을 QListView의 파생클라스 JournalView로 설정한다. 그다음 번역과 관련한 여러개의 비공개성원변수들을 설정한다. 즉

·qmPath변수는 응용프로그람의 번역화일들을 포함하는 등록부의 경로를 지정하는 QString이다.

·appTranslator변수는 현재 응용프로그람번역을 보관하는데 사용된 QTranslator객체의 지적자이다.

·QtTranslator변수는 Qt의 번역을 보관하는데 사용되는 QTranslator객체의 지적자이다.

끝으로 createActions()와 createMenus()비공개함수들을 호출하여 차림표체계를 창조하고 비공개함수 retranslateStrings()를 호출하여 사용자에게 표시하는 문자렬들을 처음으로 설정한다.

void MainWindow::createActions() {

newAct = new QAction(this);

connect(newAct, SIGNAL(activated()), this, SLOT(newFile()));

...

aboutQtAct = new QAction(this);

connect(aboutQtAct, SIGNAL(activated()), qApp, SLOT(aboutQt()));

}

createActions()함수는 보통 QAction객체들을 창조하지만 본문이나 지름건들을 설정하지 않는다. 이것들은 retranslateStrings()에서 수행한다.

void MainWindow::createMenus() {

fileMenu = new QPopupMenu(this);

newAct→addTo(fileMenu); openAct→addTo(fileMenu);

saveAct→addTo(fileMenu); exitAct→addTo(fileMenu);

...

createLanguageMenu();

}

createMenus()함수는 차림표들을 창조하지만 차림표띠에 삽입하지 않는다. 이것도 역시 retranslateStrings()에서 수행한다.

함수의 끝에서는 createLanguageMenu()를 호출하여 Language차림표를 유지된 언어들의 목록으로 채운다. 그 원천코드를 론의한다. 우선 retranslateStrings()를 론의한다.

void MainWindow::retranslateStrings() {

setCaption(tr("Call Center"));

newAct→setMenuText(tr("&New")); newAct→setAccel(tr("Ctrl+N"));

newAct→setStatusTip(tr("Create a new journal"));

...

aboutQtAct→setMenuText(tr("About &Qt"));

aboutQtAct→setStatusTip(tr("Show the Qt library's About box"));

menuBar()→clear();

menuBar()→insertItem(tr("&File"), fileMenu);

menuBar()→insertItem(tr("&Edit"), editMenu);

menuBar()→insertItem(tr("&Reports"), reportsMenu);

menuBar()→insertItem(tr("&Language"), languageMenu);

menuBar()→insertItem(tr("&Help"), helpMenu);

}

retranslateStrings()함수는 MainWindow클라스용의 모든 tr()호출이 발생하는 곳이다. 이 함수는 MainWindow구성자의 끝에서 호출되고 또한 사용자가 Language차림표에 의해 응용프로그람의 언어를 변경할 때마다 호출된다.

매개 QAction의 차림표본문, 지름건, 상태암시를 설정한다. 또한 차림표들을 번역된 이름으로 차림표띠에 삽입한다. (clear()호출은 retranslateStrings()를 한번이상 호출할 때필요하다.)

createMenus()함수는 처음에 호출된 createLanguageMenu()를 참고하여 Language차림표에 언어목록을 채운다.

void MainWindow::createLanguageMenu() {

QDir dir(qmPath);

QStringList fileNames = dir.entryList("callcenter_*.qm");

for (int i = 0;i < (int)fileNames.size();++i) {

QTranslator translator;

translator.load(fileNames[i], qmPath);

QTranslatorMessage message = translator.findMessage("MainWindow", "English");

QString language = message.translation();

int id = languageMenu→insertItem( tr("&%1 %2")

.arg(i + 1).arg(language), this, SLOT(switchToLanguage(int)));

languageMenu→setItemParameter(id, i);

if (language == "English")

languageMenu→setItemChecked(id, true);

QString locale = fileNames[i];

locale = locale.mid(locale.find('_') + 1);

locale.truncate(locale.find('.'));

locales.push_back(locale);

}

}

응용프로그람이 유지하는 언어들을 코드작성하지 않고 응용프로그람의 translations등록부에 배치된 매개 .qm화일용으로 차림표항목을 하나씩 창조한다. 단순히 영어용의 .qm화일이 있다고 가정한다. 사용자가 영어를 선택할 때 QTranslator객체들에 대하여 clear()를 선택하는 방법이 있다.

한가지 특별한 난관은 매개 .qm화일이 제공하는 언어용으로 좋은 이름을 제시하는것이다. .qm화일의 이름에 기초하여 English를 en으로 혹은 Deutsch를 de로 표시하면 미숙해보이며 일부 사용자들은 혼돈한다. createLanguageMenu()에서 사용한 방법은 MainWindow문맥에서 문자렬 "English"의 번역을 검사하는것이다. 그 문자렬은 도이췰란드어번역에서 "Deutsch"로, 프랑스어번역에서 "Français"로, 일본어번역에서 "日本語"로 번역되여야 한다.

QPopupMenu::insertItem()를 리용하여 차림표항목들을 창조한다. 이것들은 모두 기본창문의 switchToLanguage(int)처리부에 련결되는데 다음에 론의한다.

switchToLanguage(int)처리부의 파라메터는 setItemParameter()에 의해 설정한 값이다. 이것은 3장에서 표계산프로그람의 최근에 연 화일목록을 실현할 때 수행한것과 아주 비슷하다.

끝으로 switchToLanguage()을 실현하는데 사용하는 locales라고 부르는 QStringList에 지역을 추가한다.

void MainWindow::switchToLanguage(int param) {

appTranslator→load("callcenter_" + locales[param], qmPath);

QtTranslator→load("Qt_" + locales[param], qmPath);

for (int i = 0; i < (int)languageMenu→count(); ++i)

languageMenu→setItemChecked(languageMenu→idAt(i), i == param);

retranslateStrings();

}

switchToLanguage()처리부는 사용자가 Language차림표로부터 언어를 선택할 때 호출된다.

응용프로그람과 Qt용의 번역화일을 적재하는것으로 시작한다. 그다음 Language차림표항목앞의 검사표식들을 갱신하여 사용중에 있는 언어를 표식하고 retranslateStrings()를 호출하여 기본창문의 문자렬들을 모두 재번역한다.

Microsoft Windows에서 Language차림표를 제공하는 다른 수법은 환경의 지역에서 변화를 탐지할 때 Qt에 의해 발생된 사건형인 LocaleChange사건에 응답하는것이다. 사건형은 Qt에 유지된 모든 가동환경들에서 존재하지만 Windows에서는 사용자가 체계의 지역설정(Control Panel의 Regional and Language Options)을 변경할 때 실제로 생성된다. LocaleChange사건들을 조종하기 위하여 QObject::event()를 다음과 같이 재정의한다.

bool MainWindow::event(QEvent *event) {

if (event→type() == QEvent::LocaleChange) {

appTranslator→load(QString("callcenter_") + QTextCodec::locale(), qmPath);

QtTranslator→load(QString("Qt_") + QTextCodec::locale(), qmPath);

retranslateStrings();

}

return QMainWindow::event(event);

}

응용프로그람이 실행중에 있을 때 사용자가 지역을 절환하면 새 지역용의 정확한 번역화일들을 적재하고 retranslateStrings()를 호출하여 사용자대면부를 갱신한다.

모든 경우에 기초클라스중 하나가 LocaleChange사건들과 관련될수도 있으므로 기초클라스의 event()함수에 대하여 사건을 넘긴다.

이것으로 MainWindow코드의 서술을 끝낸다. 그러면 응용프로그람의 창문부분품클라스들중 하나인 JournalView클라스의 코드를 론의하여 동적번역을 유지하려면 어떤 변경이 필요한가를 론의해보자.

JournalView::JournalView(QWidget *parent, const char *name) : QListView(parent, name) {

...

retranslateStrings();

}

JournalView클라스는 QListView의 파생클라스이다. 구성자의 끝에서 비공개함수 retranslateStrings()를 호출하여 창문부분품의 문자렬들을 설정한다. 이것은 MainWindow에서 수행한것과 비슷하다.

bool JournalView::event(QEvent *event) {

if (event→type() == QEvent::LanguageChange)

retranslateStrings();

return QListView::event(event);

}

event()함수를 재정의하여 LanguageChange사건들에 대하여 retranslateStrings()를 호출한다.

Qt는 QApplication에 현재 설치된 QTranslator의 내용이 변할 때 LanguageChange사건을 생성한다. Call Center응용프로그람에서 이것은 MainWindow::switchToLanguage()나 MainWindow::event()로부터 appTranslator 혹은 QtTranslator에 대하여 load()를 호출할 때 발생한다.

LanguageChange사건들은 LocaleChange사건들과 같지 않다. LocaleChange사건은 응용프로그람에 "Maybe you should load a new translation."라고 알린다. 대조적으로 LanguageChange사건은 응용프로그람의 창문부분품들에 "Maybe you should retranslate all your strings."라고 알린다. MainWindow를 실현했을 때 LanguageChange에 응답할 필요가 없었다. 그대신에 QTranslator에 대하여 load()를 호출했을 때마다 단순히 retranslateStrings()를 호출하였다.

void JournalView::retranslateStrings() {

for (int i = columns() -1; i >= 0; --i)

removeColumn(i);

addColumn(tr("Time")); addColumn(tr("Priority"));

addColumn(tr("Phone Number")); addColumn(tr("Subject"));

}

retranslateStrings()함수는 새로 번역된 본문을 가지고 QListView의 렬제목들을 다시 창조한다. 모든 렬제목들을 삭제하고 새로운 렬제목들을 추가하고 이것을 수행한다. 이 조작은 오직 QListView제목에만 영향을 주며 QListView에 보관한 자료에는 영향을 주지 않는다.

이것으로 손으로 쓴 창문부분품의 번역관련코드의 설명을 끝낸다. Qt Designer로 개발한 창문부분품과 대화창들에서 uic도구는 LanguageChange사건들에 응답하여 자동적으로 호출되는 retranslateStrings()함수와 비슷한 함수를 자동적으로 생성한다. 이제 해야 할 일은 사용자가 언어를 절환할 때 번역화일을 적재하는것이다.

### 3. 응용프로그람의 번역

tr()호출을 포함하는 Qt응용프로그람의 번역은 3단계의 과정으로 되여있다.

① lupdate를 실행하여 사용자에게 표시하는 문자렬들을 응용프로그람의 원천코드에서 얻는다.

② Qt Linguist에 의하여 응용프로그람을 번역한다.

③ lrelease을 실행하여 응용프로그람이 QTranslator를 사용하여 적재하는 2진.qm화일을 생성한다.

걸음 ①과 ③은 응용프로그람개발자들이 수행한다. 걸음 ②는 번역기가 처리한다. 이 주기는 응용프로그람의 개발과 수명기간 필요할 때마다 반복될수 있다.

실례로 표계산프로그람을 번역하는 방법을 보기로 한다. 응용프로그람은 이미 사용자에게 표시하는 문자렬주위에 tr()호출을 포함한다.

우선 응용프로그람의 .pro화일을 수정하여 유지하려는 언어들을 지정해야 한다. 례를 들면 영어와 함께 도이췰란드어와 프랑스어를 유지하려고 한다면 다음의 TRANSLATIONS항목을 spreadsheet.pro에 추가해야 한다.

TRANSLATIONS = spreadsheet_de.ts\spreadsheet_fr.ts

여기서는 2개의 번역화일 즉 도이췰란드어화일과 프랑스어화일을 지정한다. 이 화일들은 처음으로 lupdate를 실행할 때 창조되고 후에 lupdate를 실행할 때마다 갱신된다.

보통 이 화일들은 .ts확장자를 가진다. 이것들은 간단한 XML형식으로 되여있고 QTranslator에 의해 해석된 2진.qm화일들처럼 조밀하지 않다. 사람이 읽을수 있는 .ts화일을 콤퓨터에 효과적인 .qm화일들로 변환하는것은 lrelease의 과제이다. 자세히 말하면 .ts는 번역원천화일을 의미하고 .qm은 Qt통보문화일을 의미한다.

표계산프로그람의 원천코드를 포함한 등록부안에 있다고 가정하면 spreadsheet.pro에 대하여 지령행에서 lupdate를 다음과 같이 실행할수 있다.

lupdate -verbose spreadsheet.pro

-verbose인수는 선택인수이다. 이것은 lupdate에 보통보다 반결합을 더 제공한다는것을 알린다. 여기에 기대한 출력이 있다.

Updating 'spreadsheet_de.ts'...

0 known, 101 new and 0 obsoleted messages

Updating 'spreadsheet_fr.ts'...

0 known, 101 new and 0 obsoleted messages

응용프로그람원천코드의 tr()호출안에서 나타나는 모든 문자렬은 빈 번역을 가지는 .ts화일들에 보관된다. 응용프로그람의 .ui화일들에 나타나는 문자렬들도 포함된다.

lupdate도구는 기정으로 tr()인수들이 Latin-1문자렬이라고 가정한다. 그렇지 않으면 CODEC항목을 .pro화일에 추가해야 한다. 례를 들면

CODEC = EUC-JP

이것은 응용프로그람의 main()함수로부터 QTextCodec::setCodecForTr()호출과 함께 수행되여야 한다. 그다음 Qt응용프로그람들을 번역하는 GUI도구인 Qt Linguist를 리용하여 spreadsheet_de.ts와 spreadsheet_fr.ts화일에 번역을 추가해야 한다.

Qt Linguist를 기동하려면 Windows에서는 Start차림표에서 Qt 3.2.x|Qt Linguist를 찰칵하고 Unix에서는 지령행에서 linguist라고 입력하며 Mac OS X Finder에서는 linguist를 두번 찰칵한다. .ts화일에 대한 번역추가를 시작하려면 File|Open를 찰칵하고 화일을 선택한다.

Qt Linguist기본창문의 왼쪽에 번역중에 있는 응용프로그람의 문맥목록들이 표시된다. 표계산프로그람에서 문맥들로서는 FindDialog, GoToCellDialog, MainWindow, SortDialog, Spreadsheet가 있다. 오른쪽웃구역은 현재 문맥용의 원천본문목록이다. 매개 원천본문은 번역과 Done기발과 함께 표시된다. 오른쪽 중간구역은 현재 원천항목의 번역을 입력할수 있는 곳이다. 오른쪽 아래구역은 Qt Linguist가 자동적으로 제공하는 제안목록이다.

번역된 .ts화일을 일단 얻으면 그것을 2진.qm화일로 변환하여 QTranslator가 리해할수 있게 해야 한다. 그러자면 Qt Linguist안에서 File|Release를 찰칵한다. 일반적으로 일부 문자렬만 번역하는것으로 시작하며 .qm화일을 가지고 응용프로그람을 실행하여 제대로 작업하는가 확인한다. 모든 .ts화일들에 대하여 .qm화일들을 다시 생성하려고 한다면 lrelease지령행도구를 다음과 같이 사용한다.

lrelease -verbose spreadsheet.pro

19개 문자렬을 프랑스어로 번역하고 그중 17개에 Done기발을 찰칵하였다고 가정하면 lrelease는 다음의 출력을 생성한다.

Updating 'spreadsheet_de.qm'...

0 finished, 0 unfinished and 101 untranslated messages

Updating 'spreadsheet_fr.qm'...

17 finished, 2 unfinished and 82 untranslated messages

번역하지 않은 문자렬들은 응용프로그람을 실행할 때 원래언어로 표시된다. Done기발은 lrelease가 사용하지 않으며 번역기들이 어느 번역을 끝내고 어느 번역을 다시 방문해야 하는가를 식별하는데 쓰인다.

응용프로그람의 원천코드를 수정할 때 번역화일들이 갱신될수 있다. 해결책은 lupdate를 다시 실행하고 새 문자렬들의 번역을 제공하고 .qm화일들을 다시 생성하는것이다. 일부 개발팀들은 lupdate를 자주 실행하기 좋아하며 다른 팀들은 최종제품을 출하하기 직전까지 기다리기를 좋아한다.

lupdate와 Qt Linguist도구는 아주 고급한 도구이다. 더는 사용하지 않는 번역은 후에 출하할 때 요구되는 경우에만 .ts화일들에 보관한다. .ts화일들을 갱신할 때 lupdate는 지능결합알고리듬을 사용하므로 번역기들이 각이한 문맥들에서 같거나 류사한 본문을 번역할 때 상당한 시간을 절약할수 있게 한다.

## 제5절. Plug-in

Qt에서는 Plug-in을 리용하여 Qt응용프로그람에 필요한 기능들을 확장할수 있다. Qt는 2가지 종류의 APl를 리용하여 Plug-in을 만든다.

하나는 Qt의 수준이 높은 API를 확장(례를 들어 자료기지 Plug-in, 화상 Plug-in, 양식 Plug-in 등)하는것이며 다른 하나는 Qt의 수준이 낮은 API를 리용하여 Plug-in(례를 들어 임의의 Plug-in)을 만드는것이다.

### 1. Plug–in개발의 기초

Plug-in을 리용하려면 먼저 통일적인 대면부를 정의해야 하는데 여기서는 반드시 2가지 문제를 해결하여야 한다.

하나는 프로그람에서 어떻게 Plug-in을 리용하겠는가 하는것이며 다른 하나는 어떻게 Plug-in을 만들겠는가 하는것이다.

Qt에서 Plug-in을 리용하는 순서는 다음과 같다.

① Plug-in대변부(C++에서 대면부는 순수가상함수의 추상클라스를 리용)를 정의한다.

② Q_DECLARE_lNTERFACE()마크로를 리용하여 Qt메타객체체계에 대면부정보를 등록한다.

③ 프로그람에서 QPlug-inLoader클라스를 리용하여 Plug-in을 적재한다.

④ qobject_cast()함수를 리용하여 Plug-in이 지정한 대면부를 만들었는가를 검사한다.

Qt에서 Plug-in을 만드는 순서는 다음과 같다.

① QObject와 Plug-in을 리용하여야 할 대면부에서 계승된 Plug-in클라스를 정의한다.

② Q_lNTERFACE()마크로를 리용하여 Qt메타객체체계에 대면부정보를 등록한다.

③ Q_EXPORT_PLUG-IN2()마크로를 리용하여 Plug-in을 반출한다.

④ qmake화일(.pro화일)을 창조하여 Plug-in을 만든다.

Plug-in대면부클라스를 정의하는 코드는 다음과 같다.

class Tacticslnterface {

public:

virlual ~Tacticslnterface() {}

virtual in t caJculale(inl x, int y) = 0;

}

Q_DECLARE_JNTERFACE(TacticsJnterface, “com.palace.tactics/1.0")

이 대변부클라스에서는 순수가상한수 calculate()를 정의하였는데 이 함수는 Plug-in을 프로그람에 나타내는 대면부함수이다.

Q_DECLARE_INTERPFACE()클라스는 메타객체체계에 대면부를 등록한다.

TacticsPlug-in클라스의 코드는 다음과 갈다.

class TacticsPlug-in: public QObject, public TacticsJnterface {

Q_OBJECT

Q_INTERFACES(TacticsInterface)

public:

int calculate(int x, int y)

};

TacticsPlug-in클라스에서는 Q_INTERFACES마크로를 리용하여 Qt의 메타객체체계에 대면부를 등록한다. 일반적인 프로그람에서와는 달리 Plug-in에서 오유제거(debug)는 비교적 복잡하다. 먼저 독립적인 프로그람을 개발하고 다음에 이것을 Plug-in으로 바꾸면 오유제거를 쉽게 할수 있다. Plug-in을 리용할 때 환경변수 QT_DEBUG_PLUG_IN을 령이 아닌 다른 값으로 설정하여 Plug-in의 오유제거정보를 볼수 있다.

### 2. Qt Designer Plug–in

Qt Designer에는 많은 창문부분품들이 있다. 그러나 실지 용용에서 이와 갈이 일반적인 창문부분품들은 프로그람작성자의 요구를 충분히 만족시키지 못한다. 그러므로 프로그람작성자는 Qt Designer Plug-in확장기구를 리용하여 자기의 요구를 실현한다.

만일 자체정의한 창문부분품을 리용하려면 창문부분품의 각종 기능들을 자체로 정의하여야 하며 Qt Designer에서 구체적인 창문부분품을 선택하여 이 창문부분품의 클라스를 리용하여야 한다.

Qt Designer에서 새로 ui화일을 창조하고 Dialog나 Widget에 Label창문부분품을 배치한다. 배치한 Label창문부분품에서 마우스의 오른쪽 단추률 눌러 “Promote to Custom Widget"를 선택한다. “Promoted Widgets" 대화창에서 “promoted class name" 에 MyLabel을 입력하고 “Header file"에 머리부화일의 이름을 입력한다. 이 Label은 uic를 리용하여 원천코드를 창조할 때 MyLabel클라스에 기초하여 창조된 객체로 된다.

본문편집기로“.ui화일”을 보면 이 Label은 ui화일에서 다음과 같이 서술되여있다.

<widget class= “MyLabel” name=“label”>

Qt Designer에는 4개의 확장(Extension)기능이 있다.

·과제차림표확장기능: 이 기능은 QDesignerTaskMenuExtension클라스에 기초한것으로서 Qt Designer의 오른쪽 차림표를 확장한다. 이 기능은 Qt Designer의 과제차림표에 자체정의차림표항목을 추가할수 있게 한다.

·용기확장기능: 이 기능은 QDesignerContainerExtension클라스에 기초한것으로서 multipage용기 Plug-in과 Page를 추가하고 삭제할수 있게 한다.

·성원표확정기능: 이 기능은 QDesignerMemberSheetExtension클라스에 기초한것으로서 창문부분품의 성원함수를 조작하며 신호와 처리부의 련결을 현시할수 있게 한다.

·속성페지확장기능: 이 기능은 QDesignerPropertySheetExtension클라스에 기초한것으로서 Qt Designer의 속성편집기에서 창문부분품의 속성을 조작할수 있게 한다. 확장기능을 창조하기 위하여서는 그것이 반드시 QObject와 대응한 기초클라스로부러 계승되도록 하여야 하며 대응한 함수들을 만들어야 한다.

Qt메타객체체계가 대변부를 인식하게 하기 위해 Q_INTERFACES()마크로를 리용한다.

c1ass MyExtension: public QObject, public QDesignerContainerExtension {

Q OBJECT

Q_INTERFACES(QDesignerContainerExtension)

…

}

Qt Designer는 qobject cast()함수를 리용하여 지원하는 대면부를 검사한다.

라침판 Plug-in을 만드는 프로그람은 다음과 같다.

이 Plug-in은 비행기의 방향이 바뀔 때 라침판바늘의 방향도 바뀌는 라침판을 만든다.

Plug-in은 QDesignerCustomWidgetlnterface클라스에서 계승된다.

이 클라스의 실현코드는 다음과 같다.

#include “compass.h"

#include “compassPlug-in.h"

#include <QtPlug-in>

CompassPlug-in::CompassPlug-in(QObject *parent): QObject(parent) {

m_initialized=false;

}

void CompassPlug-in::initialize(QDesignerForrnEditorlnterface * /* core */) {

if (m_initialized)

return;

m_initialized= true;

}

bool CompassPlug-in::isInitialized() const { return m_initialized; }

QWidget *CompassPlug-in::createWidget(QWidget *parent) {

return new Compass(parent);

}

QString CompassPlug-in::name() const { return “Compass”; }

QString CompassPlug-in::group() const { return “My Widgets”; }

QIcon CompassPlug-in::icon() const { return QIcon(“:/Qt.svg”); }

QString CompassPlug-in::toolTip() const { return “Compass”; }

QString CompassPlug-in::whatsThis() const { return “Compass”; }

bool CompassPlug-in::isContainer() const { retum false; }

QString CompassPlug-in::domXml() const {

return “<ui language=\” c++\” > \n”

“<widget class=\” Compass\” name= \” Compass\” >\n”

“ <property name= \” geometry\” >\n”

“ <rect>\n”

“ <x>0</x>\n”

“ <y>0</y>\n”

“ <width>100</width>\n”

“ <height>100</height>\n”

“ </rect>\n”

“ </property>\n”

“ </widgct>\n”

“ </ui>”;

}

QString CompassPlug-in::includeFile() const {return “compass.h";}

Q_EXPORT_PLUG-1N2(compassplug-in, CompassPlug-in)

createWidget()함수는 Plug-in객체를 창조한다.

name()함수는 Plug-in이름을 되돌린다.

group()함수는 Plug-in이 Qt Designer에서 어느 group에 놓이는가를 지정한다.

icon()함수는 Plug-in의 그림기호를 되돌린다.

Plug-in의 기본실현코드는 디음과 같다.

#ìnclude <QtGui>

#ìnclude <QPainter>

#ìnclude "compass. h"

const int labelX= - 8;

const ìnt labelY= -65;

Compass::Compass(QWidget *parent) : QWìdget(parent) {

setWindowTitle(tr(“Compass”));

m_angle=0; //North

m_step=0;

m_animateAngle=0;

m_second=0;

resize(200, 200);

}

// draw Compass

void Compass::paintEvent(QPaintEvent *) {

static const QPoint needle[3] = {QPoint(7, 8), QPoint(-7, 8), QPoint(0, -70)};

QColor poleColor(127, 0, 127);

QColor scaleColor(0, 127, 127, 191);

int side=qMìn(width(), height());

QPainter painter(this);

painter.setRenderHint(QPainter::Antialiasing);

painter.translate(width()/2, height()/2);

painter.scale(side/200.0, side/200.0);

painter.setPen(Qt::NoPen);

painter.setBrush(poleColor);

painter.save();

painter.drawConvexPolygon(needle, 3);

painter.restore();

painter.setPen(poleColor);

QFont font;

font.setBold(true);

font.setPointSize(18);

painter.setFont(font);

painter.rotate(-m_animateAngle);

for(int i=0; i<8;++i) {

painter.drawLine(0, -96, 0, 88);

switch(i){

case 0 :

painter.drawText(labelX, labelY, “N”);

break;

case 2:

painter.drawText(labelX, labelY, “E”);

break;

case 4:

painter.drawText(labelX, labelY, “S”);

break;

case 6:

painter.drawText(labeIX, labelY, “W”);

break;

}

painter.rotate(45.0);

}

painter.setPen(scaleColor);

for (int j=0; j<60; ++j) {

if ((j % 15) != 0)

painter.drawLine(92, 0, 96, 0);

painter.rotate(6.0);

}

}

void Compass::setValue(Qreal heading) { m_angle=heading; }

void Compass::timerEvent(QTimerEvent *event) {

m_animateAngle+= m_step;

if(m_animateAngle <= m_angle)

update();

else

killTimer(event→timerId());

}

void Compass::setSecond(int second) {

m_second = second;

m_animateAngle=0;

if(m_second <= 0)

m_step = m_angle;

else

m_sleep = m_angle / (second*30);

startTimer(50);

}

프로젝트화일(.pro화일)에는 다음의 내용을 추가하여야 한다.

TEMPLATE=lib

CONFIG += designer plug-in debug_and_release

CONFIG변수에서 designer는 프로젝트가 libQtDesigner.so(또는 QtDesigner4.d11)서고와 동적련결을 진행해야 한다는것을 나타낸다.

plug-in은 프로젝트가 창조한 목표를 Plug-in서고로 한다는것을 나타낸다.

만일 debug방식과 release방식에서 다 번역되도록 하려면 Windows체계나 Mac체계에 debug판목표실행화일에 알맞는 뒤붙이를 붙여야 한다.

정의코드는 다음과 같다.

CONFIG(debug, debug | release){

mac:TARGET=$$join(TARGET,,,_debug)

win32:TARGET=$$join(TARGET,,,d)

}

Qt Designer가 release판이므로 release판 Plug-in으로 번역하여야 Qt Designer에 라침판 Plug-in이 정확히 적재된다.

번역한 서고를 designer plug-in등록부에 넣은 다음 이 서고를 Qt Designer가 자동적으로 적재하도록 하기 위하여서는 프로젝트에 다음과 같은 명령문을 추가하여야 한다.

target.path=$$[QT_INSTALL_PLUG-INS]/designer

INSTALLS += target

make install을 실행시켜 라침판 Plug-in을 설치한다.
