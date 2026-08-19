"""프론트엔드 테스트용 샘플 리포트 3개를 reports.db에 삽입한다. 1회성 스크립트."""

from __future__ import annotations

import db

REPORTS = [
    {
        "title": "Transformer: Self-Attention만으로 구성된 시퀀스 변환 모델",
        "body_markdown": (
            "## 개요\n\n"
            "기존 시퀀스 변환(seq2seq) 모델은 RNN이나 CNN을 인코더-디코더의 기본 "
            "구성 요소로 사용했다. 그러나 RNN은 이전 타임스텝의 은닉 상태에 의존하는 "
            "순차 연산 구조 때문에 병렬화가 어렵고, 시퀀스 길이가 길어질수록 앞쪽 "
            "정보가 희석되는 문제가 있었다. 이 논문은 순환·합성곱 구조를 전부 제거하고 "
            "Self-Attention만으로 인코더와 디코더를 구성한 Transformer 아키텍처를 "
            "제안한다.\n\n"
            "## 핵심 방법론\n\n"
            "- **Scaled Dot-Product Attention**: Query, Key, Value 세 벡터로 "
            "Attention(Q, K, V) = softmax(QKᵀ / √d_k) V를 계산한다. 내적 값을 "
            "√d_k로 나누어 스케일링함으로써, 차원이 커질 때 softmax의 기울기가 "
            "지나치게 작아지는 문제를 완화한다.\n"
            "- **Multi-Head Attention**: 하나의 Attention을 쓰는 대신, Q/K/V를 "
            "여러 개의 낮은 차원 부분공간으로 나눠 h개의 헤드가 서로 다른 표현 "
            "공간에서 병렬로 Attention을 계산하고 결과를 이어붙인다(논문 기본 설정 "
            "h=8). 서로 다른 위치·관점의 관계를 동시에 포착할 수 있다.\n"
            "- **Positional Encoding**: 순환 구조가 없어 순서 정보가 사라지므로, "
            "서로 다른 주파수의 sin/cos 함수로 만든 위치 인코딩을 입력 임베딩에 "
            "더해 순서 정보를 주입한다.\n"
            "- **인코더-디코더 스택**: 각각 동일한 구조의 레이어를 6개씩 쌓고, "
            "레이어마다 Multi-Head Attention과 Position-wise Feed-Forward "
            "네트워크에 잔차 연결(residual connection)과 층 정규화(layer "
            "normalization)를 적용한다. 디코더는 미래 토큰을 보지 못하도록 "
            "마스킹된 Self-Attention과, 인코더 출력을 참조하는 Cross-Attention을 "
            "추가로 갖는다.\n\n"
            "## 주요 실험 결과\n\n"
            "WMT 2014 영어-독일어 번역에서 Transformer(Big) 모델은 BLEU 28.4점을, "
            "영어-프랑스어 번역에서는 41.8점을 기록해 기존 최고 성능 모델들을 "
            "능가했다. 특히 8개 GPU 기준 3.5일 학습만으로 이 성능을 달성해, "
            "학습 비용 대비 성능에서도 큰 개선을 보였다.\n\n"
            "## 의의와 한계\n\n"
            "순차 연산을 제거해 학습 병렬화가 가능해졌다는 점이 가장 큰 기여이며, "
            "이후 BERT·GPT 계열을 비롯한 대규모 언어모델의 표준 아키텍처로 "
            "자리잡았다. 다만 Self-Attention의 연산량과 메모리 사용량이 시퀀스 "
            "길이의 제곱에 비례해 증가하므로, 매우 긴 시퀀스를 다룰 때는 별도의 "
            "효율화 기법이 필요하다는 한계가 있다.\n"
        ),
        "papers": [
            {
                "title": "Attention Is All You Need",
                "authors": [
                    "Ashish Vaswani",
                    "Noam Shazeer",
                    "Niki Parmar",
                    "Jakob Uszkoreit",
                    "Llion Jones",
                    "Aidan N. Gomez",
                    "Łukasz Kaiser",
                    "Illia Polosukhin",
                ],
                "doi": "https://doi.org/10.48550/arXiv.1706.03762",
                "landing_page_url": "https://arxiv.org/abs/1706.03762",
                "openalex_id": "https://openalex.org/W2626778328",
            }
        ],
    },
    {
        "title": "SimCLR: 대조 학습 기반 시각 표현 학습 프레임워크",
        "body_markdown": (
            "## 개요\n\n"
            "레이블 없는 이미지로부터 downstream task에 잘 전이되는 표현을 "
            "학습하는 자기지도학습(self-supervised learning)은 오랫동안 지도학습 "
            "대비 큰 성능 격차가 있었다. 이 논문은 특수한 아키텍처나 메모리 뱅크 "
            "없이도, 몇 가지 설계 요소를 올바르게 조합하면 대조 학습만으로 지도학습에 "
            "근접한 표현을 학습할 수 있음을 보인 단순한 프레임워크 SimCLR를 "
            "제안한다.\n\n"
            "## 핵심 방법론\n\n"
            "- **데이터 증강 쌍 생성**: 하나의 이미지에 무작위 자르기·리사이즈, 색상"
            "왜곡, 가우시안 블러 등을 조합해 서로 다른 두 view를 만들고, 이를 "
            "양성(positive) 쌍으로 취급한다.\n"
            "- **Base Encoder + Projection Head**: ResNet 계열 인코더 f(·)로 "
            "표현을 얻은 뒤, 1개의 은닉층을 가진 MLP인 projection head g(·)를 "
            "거쳐 대조 손실 계산에 사용할 벡터를 얻는다. 실제 downstream task에는 "
            "g(·) 이전의 인코더 출력을 사용한다.\n"
            "- **NT-Xent 손실**: 미니배치 내 나머지 이미지들을 음성(negative) "
            "샘플로 삼아, 온도(temperature)로 스케일링한 코사인 유사도 기반 "
            "교차 엔트로피 손실로 양성 쌍의 유사도는 높이고 음성 쌍과는 멀어지도록 "
            "학습한다. 메모리 뱅크 없이 배치 내 negative만으로 학습이 가능하다.\n\n"
            "## 주요 실험 결과 및 발견\n\n"
            "데이터 증강의 '조합'(특히 무작위 자르기 + 색상 왜곡)이 표현 품질에 "
            "결정적이며, 비선형 projection head를 추가하면 표현 품질이 크게 "
            "향상됨을 확인했다. 또한 대조 학습은 지도학습보다 더 큰 배치 크기와 "
            "더 긴 학습에서 이득을 본다는 점도 밝혔다. ResNet-50(4×) 인코더 기준 "
            "ImageNet 선형 평가(linear evaluation)에서 top-1 정확도 76.5%를 "
            "기록해, 동일 구조의 지도학습 ResNet과 유사한 수준까지 격차를 좁혔다.\n\n"
            "## 의의와 한계\n\n"
            "복잡한 아키텍처 변경 없이 데이터 증강·손실 설계만으로 자기지도학습 "
            "성능을 끌어올릴 수 있음을 보여 이후 MoCo v2, BYOL 등 후속 대조 학습 "
            "연구에 큰 영향을 주었다. 다만 큰 배치 크기(논문 기준 최대 4096)와 "
            "다수의 TPU 코어가 필요해 재현·확장에 상당한 연산 자원이 든다는 한계가 "
            "있다.\n"
        ),
        "papers": [
            {
                "title": "A Simple Framework for Contrastive Learning of Visual Representations",
                "authors": [
                    "Ting Chen",
                    "Simon Kornblith",
                    "Mohammad Norouzi",
                    "Geoffrey E. Hinton",
                ],
                "doi": "https://doi.org/10.48550/arxiv.2002.05709",
                "landing_page_url": "http://arxiv.org/abs/2002.05709",
                "openalex_id": "https://openalex.org/W3005680577",
            }
        ],
    },
    {
        "title": "SHAP: Shapley Value 기반 통합 모델 해석 프레임워크",
        "body_markdown": (
            "## 개요\n\n"
            "LIME, DeepLIFT, Layer-Wise Relevance Propagation 등 모델 예측을 "
            "설명하는 다양한 피처 중요도 기법이 개별적으로 제안되어 왔지만, 서로 "
            "다른 이론적 근거를 갖고 있어 결과 해석이 일관되지 않는 문제가 있었다. "
            "이 논문은 이런 기법들이 사실 공통된 수학적 형태(additive feature "
            "attribution)를 공유한다는 점을 밝히고, 이를 협력 게임 이론의 Shapley "
            "Value로 통합한 SHAP(SHapley Additive exPlanations)를 제안한다.\n\n"
            "## 핵심 방법론\n\n"
            "- **Additive Feature Attribution**: 설명 모델을 원래 입력 피처가 "
            "있는지 없는지를 나타내는 이진 변수들의 선형 결합으로 정의하는 공통 "
            "형태로, 각 피처에 할당된 값의 합이 전체 예측 기여도가 되도록 한다.\n"
            "- **Shapley Value 기반 유일해**: 게임 이론에서 여러 참여자가 협력해 "
            "만든 성과를 각자의 기여도에 따라 공정하게 분배하는 Shapley Value "
            "개념을 피처 기여도 계산에 적용한다. local accuracy(설명값의 합이 "
            "실제 예측과 일치), missingness(존재하지 않는 피처의 기여도는 0), "
            "consistency(모델이 바뀌어 특정 피처의 기여가 커지거나 유지되면 그 "
            "피처의 설명값도 줄어들지 않아야 함) 세 성질을 모두 만족하는 해가 "
            "SHAP 값으로 유일함을 이론적으로 증명한다.\n"
            "- **효율적 근사 알고리즘**: 정확한 Shapley Value 계산은 피처 개수에 "
            "지수적으로 비용이 커지므로, 모델에 무관하게 쓸 수 있는 Kernel SHAP "
            "(가중 선형 회귀 기반 근사)과, 신경망에 특화해 DeepLIFT와 결합한 "
            "Deep SHAP 등 효율적인 근사 방법을 함께 제시한다.\n\n"
            "## 주요 결과\n\n"
            "이론적으로는 세 가지 바람직한 속성을 모두 만족하는 설명 기법이 "
            "SHAP 값뿐임을 증명했고, 실험적으로는 Kernel SHAP·Deep SHAP이 기존 "
            "기법 대비 계산 효율과 사람의 직관과의 일치도(사용자 평가 기준) "
            "측면에서 더 우수함을 보였다.\n\n"
            "## 의의와 한계\n\n"
            "서로 다른 해석 기법들을 하나의 이론적 틀로 통합해, 모델 종류에 "
            "무관하게 일관된 기준으로 예측을 설명할 수 있는 표준 도구로 자리잡았다. "
            "다만 피처 간 상관관계가 강할 때 Shapley Value의 '피처 독립' 가정이 "
            "깨져 설명이 비직관적으로 나올 수 있고, 정확한 계산은 여전히 비용이 "
            "커 대부분 근사값에 의존해야 한다는 한계가 있다.\n"
        ),
        "papers": [
            {
                "title": "A Unified Approach to Interpreting Model Predictions",
                "authors": ["Scott Lundberg", "Su‐In Lee"],
                "doi": "https://doi.org/10.48550/arxiv.1705.07874",
                "landing_page_url": "http://arxiv.org/abs/1705.07874",
                "openalex_id": "https://openalex.org/W2618851150",
            }
        ],
    },
    {
        "title": "ResNet: 잔차 연결로 매우 깊은 네트워크를 학습시키다",
        "body_markdown": (
            "## 개요\n\n"
            "신경망은 깊을수록 표현력이 커질 것으로 기대되지만, 실제로는 일정 "
            "깊이를 넘으면 그래디언트 소실과는 별개로 최적화 자체가 어려워져 "
            "오히려 얕은 네트워크보다 학습 오차가 커지는 'degradation 문제'가 "
            "나타났다. 이 논문은 잔차 연결(residual connection)을 도입해 "
            "100층, 심지어 1000층이 넘는 매우 깊은 네트워크도 안정적으로 학습할 "
            "수 있음을 보인다.\n\n"
            "## 핵심 방법론\n\n"
            "- **Residual Block**: 레이어가 목표 함수 H(x)를 직접 학습하는 대신, "
            "잔차 F(x) = H(x) − x를 학습하고 최종 출력을 F(x) + x로 만든다. "
            "블록이 항등 함수에 가깝게 수렴하는 경로가 항상 열려 있어, 깊이가 "
            "늘어나도 최적화가 쉬워진다.\n"
            "- **Identity/Projection Shortcut**: 입력과 출력의 차원이 같으면 "
            "그대로 더하는 identity shortcut을, 차원이 다르면 1×1 컨볼루션으로 "
            "맞춘 뒤 더하는 projection shortcut을 사용한다.\n"
            "- **Bottleneck 구조**: 50층 이상의 깊은 모델에서는 1×1-3×3-1×1 "
            "컨볼루션을 쌓은 bottleneck block으로 파라미터 수와 연산량을 줄인다.\n"
            "- 각 컨볼루션 뒤에 Batch Normalization을 적용해 학습을 안정화한다.\n\n"
            "## 주요 실험 결과\n\n"
            "ILSVRC 2015 이미지 분류 대회에서 152층 ResNet으로 top-5 오류율 "
            "3.57%를 기록하며 우승했고, 같은 대회의 검출·분할 트랙에서도 1위를 "
            "차지했다. CIFAR-10 실험에서는 1000층이 넘는 네트워크도 학습이 "
            "가능함을 보였다.\n\n"
            "## 의의와 한계\n\n"
            "잔차/skip connection은 이후 Transformer를 포함한 사실상 모든 "
            "현대 딥러닝 아키텍처의 표준 구성 요소가 되었다. 다만 매우 깊은 "
            "모델은 여전히 추론 비용과 메모리 사용량이 크다는 한계가 있다.\n"
        ),
        "papers": [
            {
                "title": "Deep Residual Learning for Image Recognition",
                "authors": ["Kaiming He", "Xiangyu Zhang", "Shaoqing Ren", "Jian Sun"],
                "doi": "https://doi.org/10.1109/cvpr.2016.90",
                "landing_page_url": "https://doi.org/10.1109/cvpr.2016.90",
                "openalex_id": "https://openalex.org/W2194775991",
            }
        ],
    },
    {
        "title": "BERT: 양방향 문맥을 사전학습하는 언어 표현 모델",
        "body_markdown": (
            "## 개요\n\n"
            "Word2Vec·GloVe 같은 정적 단어 임베딩은 문맥을 반영하지 못하고, "
            "GPT 계열은 Transformer 디코더 기반으로 왼쪽에서 오른쪽으로만 문맥을 "
            "본다는 한계가 있었다. 이 논문은 Transformer 인코더만으로 문장의 "
            "양쪽 문맥을 동시에 반영하는 사전학습 방법을 제안하고, 이를 다양한 "
            "NLP 태스크에 파인튜닝만으로 적용할 수 있음을 보인다.\n\n"
            "## 핵심 방법론\n\n"
            "- **Masked Language Model(MLM)**: 입력 토큰의 15%를 무작위로 "
            "[MASK] 처리하고 이를 예측하도록 학습한다. 이렇게 하면 좌우 문맥을 "
            "모두 사용해도 정답을 미리 볼 수 없어, 완전한 양방향 사전학습이 "
            "가능해진다.\n"
            "- **Next Sentence Prediction(NSP)**: 두 문장이 실제로 이어지는 "
            "문장인지 아닌지를 이진 분류로 학습해 문장 간 관계를 반영하는 표현을 "
            "함께 학습한다(이후 연구들에서 효과가 제한적이라는 지적도 있었다).\n"
            "- **사전학습 후 파인튜닝**: 사전학습된 BERT에 태스크별 얇은 출력층 "
            "하나만 추가하면, 분류·질의응답·개체명 인식 등 서로 다른 태스크에 "
            "동일한 아키텍처로 파인튜닝할 수 있다.\n\n"
            "## 주요 실험 결과\n\n"
            "GLUE 벤치마크의 여러 태스크에서 당시 최고 성능을 경신했고, SQuAD "
            "v1.1 질의응답 태스크에서는 사람 수준에 근접하거나 이를 넘는 F1 "
            "점수를 달성했다.\n\n"
            "## 의의와 한계\n\n"
            "'사전학습 후 파인튜닝' 패러다임을 NLP 전반의 표준으로 만들었고, "
            "RoBERTa·ALBERT·DistilBERT·BioBERT 등 수많은 후속 모델을 낳았다. "
            "다만 3억 개 이상의 파라미터로 학습·추론 비용이 크고, 입력 길이가 "
            "512 토큰으로 제한된다는 한계가 있다.\n"
        ),
        "papers": [
            {
                "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
                "doi": "https://doi.org/10.18653/v1/N19-1423",
                "landing_page_url": "https://aclanthology.org/N19-1423/",
                "openalex_id": "https://openalex.org/W2963341956",
            }
        ],
    },
    {
        "title": "GAN: 생성자와 판별자가 경쟁하며 학습하는 생성 모델",
        "body_markdown": (
            "## 개요\n\n"
            "기존 생성 모델은 확률분포를 명시적으로 가정하고 정규화 상수를 "
            "계산하거나 근사 추론에 의존해야 하는 경우가 많았다. 이 논문은 "
            "생성자(Generator)와 판별자(Discriminator)라는 두 신경망이 서로 "
            "경쟁하는 적대적 학습(adversarial training) 구조를 제안해, 명시적 "
            "확률분포 가정 없이 역전파만으로 실제와 구분하기 어려운 데이터를 "
            "생성할 수 있음을 보인다.\n\n"
            "## 핵심 방법론\n\n"
            "- **Generator**: 무작위 노이즈 벡터 z를 입력받아 실제 데이터와 "
            "유사한 가짜 샘플을 생성한다.\n"
            "- **Discriminator**: 실제 데이터와 Generator가 만든 가짜 데이터를 "
            "구별하도록 학습되는 이진 분류기다.\n"
            "- **Minimax 게임**: G는 D가 가짜를 진짜로 착각하도록, D는 진짜와 "
            "가짜를 정확히 구별하도록 서로 반대 방향의 목적함수를 동시에 "
            "최적화한다. 이론적으로 균형점에서는 생성 분포가 실제 데이터 분포와 "
            "일치해, D는 항상 1/2 확률로만 구별할 수 있게 된다.\n"
            "- 별도의 마르코프 체인이나 근사 추론 없이 표준 역전파만으로 학습이 "
            "가능하다.\n\n"
            "## 주요 실험 결과\n\n"
            "MNIST, TFD(Toronto Face Database), CIFAR-10 등에서 당시 다른 "
            "생성 모델보다 시각적으로 선명한 샘플을 만들어낼 수 있음을 보였다 "
            "(정성적 평가 위주).\n\n"
            "## 의의와 한계\n\n"
            "이후 DCGAN·CycleGAN·StyleGAN 등 수많은 변형을 낳으며 이미지 생성 "
            "분야의 핵심 패러다임이 되었다. 다만 Generator와 Discriminator의 "
            "균형이 쉽게 무너져 학습이 불안정하고, mode collapse(다양성 붕괴) "
            "가 자주 발생한다는 한계가 이후 여러 연구에서 지적되었다.\n"
        ),
        "papers": [
            {
                "title": "Generative Adversarial Networks",
                "authors": [
                    "Ian Goodfellow",
                    "Jean Pouget-Abadie",
                    "Mehdi Mirza",
                    "Bing Xu",
                    "David Warde-Farley",
                    "Sherjil Ozair",
                    "Aaron Courville",
                    "Yoshua Bengio",
                ],
                "doi": "https://doi.org/10.48550/arXiv.1406.2661",
                "landing_page_url": "https://arxiv.org/abs/1406.2661",
                "openalex_id": "https://openalex.org/W4298289240",
            }
        ],
    },
    {
        "title": "Adam: 모멘텀과 적응적 학습률을 결합한 최적화 알고리즘",
        "body_markdown": (
            "## 개요\n\n"
            "SGD·AdaGrad·RMSProp 등 기존 확률적 최적화 기법은 각각 한계가 "
            "있었다. AdaGrad는 학습이 진행될수록 유효 학습률이 지나치게 작아지고, "
            "RMSProp은 이를 완화하지만 모멘텀이 없어 최적화 경로가 불안정할 수 "
            "있다. 이 논문은 그래디언트의 1차 모멘트(모멘텀)와 2차 모멘트(적응적 "
            "학습률)를 함께 활용하는 Adam(Adaptive Moment Estimation)을 "
            "제안한다.\n\n"
            "## 핵심 방법론\n\n"
            "- **1차 모멘트 추정(m_t)**: 그래디언트의 지수이동평균으로, 모멘텀과 "
            "같은 역할을 한다.\n"
            "- **2차 모멘트 추정(v_t)**: 그래디언트 제곱의 지수이동평균으로, "
            "파라미터마다 다른 적응적 학습률을 만든다.\n"
            "- **Bias Correction**: 학습 초반 m_t, v_t가 0으로 초기화되어 "
            "생기는 편향을 보정하는 항을 추가한다.\n"
            "- **파라미터 업데이트**: θ = θ − α · m̂_t / (√v̂_t + ε) 형태로, "
            "파라미터마다 자동으로 다른 유효 학습률이 적용된다.\n\n"
            "## 주요 실험 결과\n\n"
            "로지스틱 회귀, 다층 퍼셉트론, CNN 등 다양한 모델과 데이터셋에서 "
            "SGD·AdaGrad·RMSProp 대비 더 빠르고 안정적으로 수렴함을 실험적으로 "
            "보였다.\n\n"
            "## 의의와 한계\n\n"
            "하이퍼파라미터에 상대적으로 덜 민감해 별도 튜닝 없이도 잘 동작하는 "
            "경우가 많아, 사실상 딥러닝 학습의 기본 옵티마이저로 자리잡았다. "
            "다만 일부 태스크에서 SGD+모멘텀 대비 일반화 성능이 떨어질 수 있다는 "
            "후속 연구들이 있었고, 이후 가중치 감쇠를 분리한 AdamW가 널리 "
            "쓰이게 되었다.\n"
        ),
        "papers": [
            {
                "title": "Adam: A Method for Stochastic Optimization",
                "authors": ["Diederik P. Kingma", "Jimmy Ba"],
                "doi": "https://doi.org/10.48550/arxiv.1412.6980",
                "landing_page_url": "https://arxiv.org/abs/1412.6980",
                "openalex_id": "https://openalex.org/W1522301498",
            }
        ],
    },
    {
        "title": "AlexNet: GPU로 학습한 깊은 CNN이 컴퓨터 비전을 바꾸다",
        "body_markdown": (
            "## 개요\n\n"
            "이 논문 이전까지 ImageNet 규모의 이미지 분류에서는 SVM이나 얕은 "
            "신경망 기반 방법이 주류였고, 깊은 CNN은 학습이 어렵고 비용이 크다고 "
            "여겨졌다. 이 논문은 GPU 병렬 연산을 활용해 8층 CNN을 성공적으로 "
            "학습시켜, 딥러닝이 컴퓨터 비전에서 실질적 우위를 가짐을 대규모 "
            "대회를 통해 처음으로 입증했다.\n\n"
            "## 핵심 방법론\n\n"
            "- **ReLU 활성화 함수**: 기존 tanh·sigmoid보다 학습 속도를 크게 "
            "개선한다.\n"
            "- **2-GPU 모델 병렬화**: 당시 GPU 메모리 한계를 우회하기 위해 "
            "네트워크를 두 GPU에 나누어 학습한다.\n"
            "- **Dropout**: 완전연결층에 적용해 과적합을 줄인다.\n"
            "- **Local Response Normalization·Overlapping Pooling·데이터 "
            "증강**(random crop, 좌우 반전, PCA 기반 색상 변형)으로 일반화 "
            "성능을 높인다.\n\n"
            "## 주요 실험 결과\n\n"
            "ILSVRC-2012 이미지 분류 대회에서 top-5 오류율 15.3%를 기록해, "
            "2위(26.2%)와 큰 격차로 우승했다.\n\n"
            "## 의의와 한계\n\n"
            "이 결과를 계기로 컴퓨터 비전 연구의 중심이 손으로 설계한 특징에서 "
            "딥러닝 기반 표현 학습으로 급격히 옮겨갔고, VGGNet·GoogLeNet·"
            "ResNet 등 후속 CNN 발전의 출발점이 되었다. 다만 완전연결층 "
            "파라미터 비중이 커 모델 크기가 크고, 8층이라는 비교적 얕은 구조는 "
            "이후 더 깊은 네트워크들에 곧 성능이 추월당했다.\n"
        ),
        "papers": [
            {
                "title": "ImageNet Classification with Deep Convolutional Neural Networks",
                "authors": ["Alex Krizhevsky", "Ilya Sutskever", "Geoffrey E. Hinton"],
                "doi": "https://doi.org/10.1145/3065386",
                "landing_page_url": "https://doi.org/10.1145/3065386",
                "openalex_id": "https://openalex.org/W3147600416",
            }
        ],
    },
    {
        "title": "OpenAlex: 완전히 개방된 학술 문헌 그래프",
        "body_markdown": (
            "## 개요\n\n"
            "학술 문헌 메타데이터는 오랫동안 Web of Science·Scopus 같은 폐쇄형·"
            "유료 데이터베이스가 지배해 왔다. 이 논문은 논문·저자·소속기관·저널/"
            "학회·연구 주제(concept)를 완전히 개방된 형태로 제공하는 대규모 학술 "
            "그래프 OpenAlex를 소개한다. Microsoft Academic Graph(MAG)가 "
            "서비스를 종료하며 남긴 공백을 메우는 오픈소스 대안으로 시작되었다. "
            "이 프로젝트의 논문 검색 Tool도 바로 이 OpenAlex API를 사용한다.\n\n"
            "## 핵심 방법론\n\n"
            "- **개체 그래프 구조**: Works(논문), Authors(저자), Sources(저널·"
            "학회), Institutions(기관), Concepts(연구 주제) 다섯 종류의 개체와 "
            "그 사이의 관계(인용, 소속, 게재 등)를 하나의 그래프로 표현한다.\n"
            "- **데이터 통합**: Crossref, ORCID, ROR, MAG 스냅샷, 각 출판사·"
            "리포지터리 메타데이터 등 여러 오픈 소스를 자동으로 수집·매칭·중복 "
            "제거해 하나의 데이터셋으로 통합한다.\n"
            "- **완전 개방 접근**: 전체 데이터셋을 무료로 내려받을 수 있고, "
            "REST API로도 무료로 조회할 수 있어 라이선스 제약 없이 연구·서비스 "
            "개발에 활용할 수 있다.\n"
            "- **Concept 자동 태깅**: 각 논문에 계층적 연구 주제를 자동으로 "
            "태깅해, 특정 분야의 논문만 걸러보거나 분야별 통계를 낼 수 있게 "
            "한다.\n\n"
            "## 주요 내용\n\n"
            "발표 당시 기준 2억 편 이상의 논문과 이에 연결된 저자·기관·인용 "
            "정보를 담고 있었으며 이후로도 계속 갱신되고 있다. 다만 후속 비교 "
            "연구들에서 Web of Science·Scopus 대비 커버리지와 메타데이터 "
            "정확도에 일부 차이가 있다는 점도 함께 보고되었다.\n\n"
            "## 의의와 한계\n\n"
            "연구비나 기관 구독 없이도 대규모 학술 데이터에 접근할 수 있는 길을 "
            "열어, 이 프로젝트처럼 개인이나 소규모 팀이 만드는 연구 지원 도구의 "
            "데이터 기반이 될 수 있게 했다. 다만 자동 매칭·중복 제거 과정에서 "
            "생기는 오류나 결측 필드가 있어(이 리포트 모음에서도 BERT 논문의 "
            "제목 필드가 비어 있어 검색으로 찾지 못하는 사례를 직접 확인했다) "
            "활용 시 결과 검증이 필요하다.\n"
        ),
        "papers": [
            {
                "title": "OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts",
                "authors": ["Jason R Priem", "Heather Piwowar", "Richard A. Orr"],
                "doi": "https://doi.org/10.5281/zenodo.6936227",
                "landing_page_url": "https://doi.org/10.5281/zenodo.6936227",
                "openalex_id": "https://openalex.org/W4288680697",
            }
        ],
    },
]


def main() -> None:
    db.init_db()
    for report in REPORTS:
        report_id = db.save_report(
            report["title"], report["body_markdown"], report["papers"]
        )
        print(f"saved report_id={report_id}: {report['title']}")


if __name__ == "__main__":
    main()
