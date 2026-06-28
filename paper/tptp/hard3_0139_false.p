% hard3_0139  eq1=1072 eq2=107  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(X,f(X,X)),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,Y),X)) )).
