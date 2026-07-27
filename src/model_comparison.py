import math

def information_criteria(rss,n,k):
    rss=max(float(rss),1e-300)
    if n<=k+1: raise ValueError("Need n > k + 1")
    base=n*math.log(rss/n); aic=base+2*k; aicc=aic+(2*k*(k+1))/(n-k-1); bic=base+k*math.log(n)
    return {'rss':rss,'aic':aic,'aicc':aicc,'bic':bic}
