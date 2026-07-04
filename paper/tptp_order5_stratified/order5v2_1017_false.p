% order5v2_1017  eq1=9697 eq2=45299  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(Z,f(X,Y)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(f(Y,Z),X),Z)) )).
