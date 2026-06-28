% hard3_0005  eq1=34 eq2=3556  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(Y,f(f(Y,X),Y)) )).
