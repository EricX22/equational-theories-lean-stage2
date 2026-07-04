% order5_0092  eq1=8417 eq2=21643  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(X,f(f(f(X,Y),X),Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(X,Z)),f(X,f(Z,X))) )).
