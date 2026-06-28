% hard3_0081  eq1=623 eq2=1035  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(X,f(f(Y,Y),Y))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(Y,f(X,X)),X)) )).
