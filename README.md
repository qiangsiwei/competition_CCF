危害公共安全事件的关联关系挖掘及预测
=============

本项目荣获第二届中国大数据技术创新大赛第一名    
代码主页  https://github.com/qiangsiwei/CCFBDG_2014

公共安全是社会尺度下公民得到的外部环境和秩序的保障，其管理水平在一定程度上反映了一个国家或地区的公共服务水平。近年来，由于国内不同地区收入差距的加大、以及周边政治环境的动荡，危害公共安全的事件时有发生，给公民个人生命和财产带来了严重损害；同时互联网技术的普及使得事件消息的传播不再受空间限制，传播行为也更为复杂，给传统的公共安全管理模式带来了巨大挑战。针对这一需求，本项目提出一种基于多维（时间、空间、语义）数据分析的公共安全事件管理方法，包括同类、异类事件的相关性分析、以及预测未来一段时间内同地区发生类似事件的可能性。研究首先基于公开的新闻和微博报道数据，结合其他多种数据源（如地区人口分布数据、GDP数据等），对公交车爆炸、暴力恐怖、以及幼儿园砍杀三类事件进行识别和提取；然后通过相关性分析与数据可视化的方法，对已提取事件的媒体传播规律、事件发生的时空共性进行分析研究；最后通过特征工程方法对时间、空间、语义特征进行提取，并采用Gradient-Boosting算法对未来一段时间内某地区公共安全事件是否发生进行预测，同时利用回归树（Regression Trees）算法对该地区发生的频次进行预测。交叉验证的实验结果表明，提出的方法能够揭示在不同时空尺度下事件发生的内在联系，对多类事件在未来1～3个月内发生次数的预测准确度达到65%~82%，充分展示了该方法在以预防为主的新型公共安全事件管理中的重要意义。

数据采集与数据集
----

针对本课题，共有3个核心数据集合    
*   新闻和微博数据集    
*   新闻传播信息数据集    
*   微博用户资料数据集    

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/01.png)

基于语义的事件提取算法
----

新闻分类与聚类算法思想如图，具体可参考论文相关章节。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/02.png)

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/03.png)

事件关联分析
----

(1)	时间触发关系研究    
同系列事件在时间上存在一定的触发关系。在一定时间范围内，一起系列危害公共安全事件的发生很可能会对另一起事情的发生产生触发作用。本项目使用最大信息量相关系数(MIC)对公交车爆炸事件、暴力恐怖事件、校园砍杀事件3类事件进行了时间维度相关性分析。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/04.png)

(2)空间触发关系研究    
首先以省级单位为空间划分单位对各个省危害公共安全事件发生频次做相关性分析，但并未发现明显的相关性特征，然而当将地理分区作为空间划分单位，每个地理分区依照空间位置含若干个省，对各个地理分区事件发生频次做相关性分析，发现各地区事件发生频次之间具有较为明显的相关性特征。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/05.png)

(3)新闻媒体传播触发关系研究    
首先可做如下定义：当日媒体报导量超过200的危害公共安全事件称为大事件，而日媒体报导量小于200的事件称为小事件。如图为公交爆炸危害公共安全事件新闻媒体传播量随时间变化规律图，可以发现，在没有大事件发生时，往往在全国范围内很少有危害公共安全事件的发生，即使有也是程度很小的事件(日媒体报道量小于10)。然而当发生一起大事件时，新闻媒体会把这件事件以很快的速度传播到全国各地，而这种媒体的传播会带动同系列事件的发生，甚至会触发另一起大事件的发生。可见新闻媒体的传播对同系列事件的发生具有较大影响。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/06.png)

(4)不同系列事件共性分析    
从图中可以看出三类危害公共安全事件均在工作日发生次数的较多，而在双休日发生次数的较少。而从节日分布的角度来看，元旦、除夕、建党节等均是三类危害公共安全事件的多发时段。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/07.png)

从三类事件的发生次数空间分布图中可以看出：公交车爆炸事件多发生于华东地区，包括山东、江苏、浙江以及福建、广东等省；校园砍杀事件多发生于西部边境省份，包括新疆自治区、云南省；校园砍杀事件则多分布于中国南方地区，河南、广东、江苏等省。如图为公交爆炸危害公共安全事件对应的空间分布图。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/08.png)

数据动态可视化如图。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/09.png)

事件预测
----

如图为公共安全事件的特征空间，可见不同维度的特征之间存在较高的互信息，包含了有价值信息。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/10.png)

通过关联分析的方法发现了同系列事件在时间、空间、媒体三个维度的触发关系，以及不同系列事件之间的共性。得到了一些结论与规律。总结起来主要有以下规律：

*   某区域（省）内某类事件在当月是否发生以及发生的次数与同类事件在该区域（省）或全国在前期（近一个月内）是否发生与发生次数有较高的相关性，通常相近的事件段，事件的发生具有一定关联性。   
*   某区域（省）内某类事件在当月是否发生以及发生次数与前期（近一个月内），同类事件在全国发生的区域的分布相关，通常相近的区域事件的发生具有相同的趋势。   
*   某区域（省）内某类事件在当月是否发生以及发生次数与前期（近一个月内）媒体对该类事件的报道以及社会舆论有一定关系（诸如媒体大规模报道、网民舆论传播带来的启发和情绪影响等）。   
*   某区域（省）内某类事件在当月是否发生以及发生次数与当月的时间特征相关，通常事件的发生按年可能具有周期性，此外也可能与当月所涉及的重大节日相关联，通常节日前后也是事件的高发期。   
*   某区域（省）内某类事件在当月是否发生以及发生次数与该区域（省）的空间地点特征相关，空间地点特征包括：该类事件在本区域内过去发生的频率，本区域的经济发展情况（通过GDP衡量）、人口数量、民族组成等。   

因此，根据前文的分析，可以将某类事件发生的可能影响因素归为5大类：   
*   前期时间（发生频率，距离上一次发生的时长）因素，对应规律（1）   
*   前期空间（事件发生点的空间分布）因素，对应规律（2）   
*   前期媒体因素（媒体报道量，社会舆论情绪），对应规律（3）   
*   本期时间（月份、季节、是否包含重大节日）因素，对应规律（4）   
*   本期空间（本地过往该事件发生的频率，经济水平，人口数量和民族组成）因素，对应规律（5）   

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/11.png)

由于事件的发生具有离散性的特点，因此，针对某区域、某时间段内事件的发生，主要对事件是否发生、事件发生频次，这两个指标进行预测。   
*   事件是否发生预测   
*   事件发生频次预测   

预测整体思想如图。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/12.png)

三类事件误报率和漏报率如表所示。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/13.png)

不同评估算法所得结果如表所示。

![Alt Text](https://raw.githubusercontent.com/qiangsiwei/competition_CCF/master/figure/14.png)

代码清单
----

*   文本事件分类    
event_classify.py    
	news_classification # 新闻分类    
	weibo_classification # 微博分类    

*   独立事件提取    
event_classify.py    
	event_extraction # 独立事件提取    
	event_feature_extraction # 独立事件特征抽取    

*   特征抽取    
feature_extract.py    

*   事件预测    
event_predict.py    
