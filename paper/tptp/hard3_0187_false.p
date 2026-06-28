% hard3_0187  eq1=1669 eq2=1472  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Z,Y),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,Y),f(Z,f(Z,W))) )).
