% hard3_0149  eq1=1232 eq2=3740  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(X,f(f(f(X,Y),Y),Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(X,Z),f(Z,Y)) )).
