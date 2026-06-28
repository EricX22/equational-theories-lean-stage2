% hard3_0087  eq1=648 eq2=3067  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(X,Y),X),X),Z) )).
