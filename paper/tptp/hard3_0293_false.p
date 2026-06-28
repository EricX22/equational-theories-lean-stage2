% hard3_0293  eq1=2787 eq2=466  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Y,X)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(Y,f(X,f(X,f(Y,X)))) )).
