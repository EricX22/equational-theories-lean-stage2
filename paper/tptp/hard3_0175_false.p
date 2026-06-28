% hard3_0175  eq1=1560 eq2=4121  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(X,f(Z,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(X,X),Y),Y) )).
