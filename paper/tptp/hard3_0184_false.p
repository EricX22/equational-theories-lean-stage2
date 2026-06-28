% hard3_0184  eq1=1661 eq2=3078  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Y,Z),Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(f(X,Y),Y),Y),X) )).
