% hard3_0014  eq1=59 eq2=3086  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(X,Y),Z),X),Y) )).
