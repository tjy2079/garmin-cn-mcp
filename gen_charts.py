"""Generate Chinese-language analysis charts for social media."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "Arial"],
    "axes.unicode_minus": False,
    "axes.facecolor": "#0f0f1a",
    "figure.facecolor": "#0f0f1a",
    "axes.edgecolor": "#2a2a3a",
    "axes.labelcolor": "#cccccc",
    "text.color": "#cccccc",
    "xtick.color": "#999999",
    "ytick.color": "#999999",
    "grid.color": "#1a1a2e",
    "grid.alpha": 0.5,
    "legend.facecolor": "#1a1a2e",
    "legend.edgecolor": "#2a2a3a",
    "legend.labelcolor": "#cccccc",
    "figure.dpi": 150,
})


def chart_1():
    """四速对比：轻松跑 vs 全马 vs 10K vs 5K"""
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ["步频\n(spm)", "步幅\n(cm)", "触地时间\n(ms)", "垂直比\n(%)", "功率体重比\n(W/kg)"]
    easy    = [180, 129, 225, 7.1, 5.6]
    mara    = [186, 154, 195, 6.1, 6.2]
    tenk    = [187, 169, 189, 5.5, 6.6]
    fivek   = [191, 177, 186, 5.1, 6.95]
    x = np.arange(len(metrics)); w = 0.2
    ax.bar(x-1.5*w, easy, w, label="轻松跑 (4:16/km)", color="#4ecdc4")
    ax.bar(x-0.5*w, mara, w, label="全马 2:27 (4:48/km)", color="#45b7d1")
    ax.bar(x+0.5*w, tenk, w, label="10K PB 31:48 (3:11/km)", color="#f7dc6f")
    ax.bar(x+1.5*w, fivek, w, label="5K PB 15:14 (3:03/km)", color="#e74c3c")
    for i, v in enumerate(fivek):
        ax.text(i+1.5*w, v+1, str(v), ha="center", fontsize=8, color="#e74c3c", fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=10)
    ax.set_title("同一双腿，四个速度", fontsize=16, fontweight="bold", color="#fff", pad=15)
    ax.legend(fontsize=9, loc="upper right"); ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT/"chart_1_four_speeds.png", facecolor="#0f0f1a"); plt.close()


def chart_2():
    """5K PB 每圈分析"""
    laps = list(range(1,14))
    pace = [2.88,3.02,3.05,3.02,3.08,3.05,3.05,3.07,3.10,3.10,3.12,2.90,2.68]
    cad  = [183,192,192,191,190,191,190,190,190,190,190,195,203]
    stride=[191,179,177,177,175,175,174,174,175,175,175,183,196]
    gct  = [184,186,186,186,187,187,187,187,187,187,187,184,175]
    fig, axes = plt.subplots(2,2,figsize=(12,8))
    data = [
        ("配速 (min/km)", pace, "#e74c3c"),
        ("步频 (spm)", cad, "#3498db"),
        ("步幅 (cm)", stride, "#2ecc71"),
        ("触地时间 (ms)", gct, "#f39c12"),
    ]
    for ax,(title,vals,c) in zip(axes.flat,data):
        ax.plot(laps,vals,color=c,linewidth=2,marker="o",markersize=4)
        ax.fill_between(laps,vals,alpha=0.15,color=c)
        ax.set_title(title,fontsize=12,color="#fff")
        ax.set_xlabel("圈 (400m)",fontsize=9,color="#666")
        ax.grid(alpha=0.3)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.annotate(str(vals[0]),(1,vals[0]),textcoords="offset points",xytext=(0,10),fontsize=8,color=c,ha="center")
        ax.annotate(str(vals[-1]),(13,vals[-1]),textcoords="offset points",xytext=(0,10),fontsize=8,color=c,ha="center")
    fig.suptitle("5K PB 15:14 — 每一圈放在显微镜下",fontsize=15,fontweight="bold",color="#fff",y=0.98)
    fig.tight_layout()
    fig.savefig(OUT/"chart_2_five_k_laps.png",facecolor="#0f0f1a"); plt.close()


def chart_3():
    """双阈值"""
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5))
    # 早课
    blocks=["第1组","第2组","第3组","第4组"]
    mp=[3.45,3.40,3.38,3.30]; mhr=[160,164,162,171]
    a1t=ax1.twinx()
    ax1.bar(blocks,mp,color="#3498db",alpha=0.8,width=0.5)
    a1t.plot(blocks,mhr,"o-",color="#e74c3c",linewidth=2,markersize=8)
    ax1.set_ylabel("配速 (min/km)",fontsize=10,color="#3498db")
    a1t.set_ylabel("心率 (bpm)",fontsize=10,color="#e74c3c")
    ax1.set_title("早课 4×5min 阈值",fontsize=12,color="#fff")
    ax1.grid(alpha=0.3); ax1.spines["top"].set_visible(False)
    for i,(b,p) in enumerate(zip(blocks,mp)): ax1.text(i,p+0.02,f"{p:.2f}",ha="center",fontsize=9,color="#fff")
    # 午课
    sets=["1","2","3","4","5","6","7"]
    at=[2.50,2.52,2.49,2.44,2.49,2.49,2.30]; ahr=[157,168,165,175,169,170,179]
    a2t=ax2.twinx()
    ax2.bar(sets,at,color="#2ecc71",alpha=0.8,width=0.5)
    a2t.plot(sets,ahr,"o-",color="#e74c3c",linewidth=2,markersize=8)
    ax2.set_ylabel("800m 成绩 (分:秒)",fontsize=10,color="#2ecc71")
    a2t.set_ylabel("心率 (bpm)",fontsize=10,color="#e74c3c")
    ax2.set_title("午课 7×800m 间歇",fontsize=12,color="#fff")
    ax2.grid(alpha=0.3); ax2.spines["top"].set_visible(False)
    for i,(s,t) in enumerate(zip(sets,at)): ax2.text(i,t+0.01,f"{t:.2f}",ha="center",fontsize=9,color="#fff")
    fig.suptitle("双阈值 — 5月7日 西安",fontsize=15,fontweight="bold",color="#fff",y=1.02)
    fig.tight_layout()
    fig.savefig(OUT/"chart_3_double_threshold.png",facecolor="#0f0f1a"); plt.close()


def chart_4():
    """10K vs 5K 对比"""
    metrics=["配速\n(min/km)","步频\n(spm)","步幅\n(cm)","触地时间\n(ms)","垂直比\n(%)","功率体重比\n(W/kg)"]
    tenk=[3.18,187,169,189,5.5,6.6]
    fivek=[3.05,191,177,186,5.1,6.95]
    delta=[round((f-t)/t*100,1) for t,f in zip(tenk,fivek)]
    fig,ax=plt.subplots(figsize=(10,5))
    x=np.arange(len(metrics)); w=0.35
    ax.bar(x-w/2,tenk,w,label="10K PB 31:48",color="#f7dc6f",alpha=0.9)
    ax.bar(x+w/2,fivek,w,label="5K PB 15:14",color="#e74c3c",alpha=0.9)
    for i,d in enumerate(delta):
        sign="+" if d>0 else ""; c="#e74c3c" if d>0 else "#2ecc71"
        ax.text(i,max(tenk[i],fivek[i])+2,f"{sign}{d}%",ha="center",fontsize=9,color=c,fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(metrics,fontsize=11)
    ax.set_title("10K vs 5K：95% 强度的自己",fontsize=16,fontweight="bold",color="#fff",pad=15)
    ax.legend(fontsize=10,loc="upper right"); ax.grid(axis="y",alpha=0.3)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT/"chart_4_ten_k_vs_five_k.png",facecolor="#0f0f1a"); plt.close()


def chart_5():
    """睡眠趋势"""
    dates=["5/4","5/5","5/6","5/7","5/8","5/9","5/10"]
    hours=[6.4,6.2,5.0,6.8,5.5,3.0,5.0]
    scores=[59,71,44,70,55,41,56]
    fig,ax=plt.subplots(figsize=(8,4)); axt=ax.twinx()
    ax.bar(dates,hours,color="#3498db",alpha=0.7,width=0.5)
    axt.plot(dates,scores,"o-",color="#e74c3c",linewidth=2,markersize=10,markerfacecolor="#e74c3c",markeredgecolor="#fff",markeredgewidth=1)
    ax.axhline(y=8,color="#2ecc71",linestyle="--",alpha=0.5,linewidth=1)
    ax.text(6.5,8.2,"目标 8h",fontsize=9,color="#2ecc71")
    ax.set_ylabel("时长 (小时)",fontsize=10,color="#3498db")
    axt.set_ylabel("评分",fontsize=10,color="#e74c3c")
    ax.set_title("睡眠：缺失的那块拼图",fontsize=14,fontweight="bold",color="#fff",pad=10)
    ax.grid(alpha=0.3); ax.spines["top"].set_visible(False)
    for i,(d,s) in enumerate(zip(dates,scores)):
        axt.annotate(str(s),(i,s),textcoords="offset points",xytext=(0,12),fontsize=9,color="#e74c3c",ha="center",fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT/"chart_5_sleep.png",facecolor="#0f0f1a"); plt.close()


if __name__=="__main__":
    print("生成中...")
    chart_1(); chart_2(); chart_3(); chart_4(); chart_5()
    print(f"完成！保存在 {OUT}")
