% order5_0175  eq1=44036 eq2=55124  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(W,X),f(W,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Y)) != f(Z,f(f(X,W),X)) )).
