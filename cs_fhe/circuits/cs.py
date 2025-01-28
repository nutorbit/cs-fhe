from concrete import fhe


def univariate_noise_reset(x):
   return fhe.univariate(lambda x: x)(x)


def multivariate_noise_reset(x):
    return fhe.multivariate(lambda x: x)(x)


@fhe.module()
class CreditScoreAveraging:
    # @fhe.function({"x": "encrypted"})
    # def bank(x):
    #     return univariate_noise_reset(x)
    
    # @fhe.function({"x": "encrypted"})
    # def telco(x):
    #     return univariate_noise_reset(x)
    
    @fhe.function({"x": "encrypted", "y": "encrypted"})
    def add(x, y):
        return univariate_noise_reset(x + y)
    
    @fhe.function({"x": "encrypted"})
    def half(x):
        return multivariate_noise_reset(x // 2)
