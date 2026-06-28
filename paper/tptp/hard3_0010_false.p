% hard3_0010  eq1=49 eq2=3867  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(X,f(Y,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(X,f(Y,X)),X) )).
