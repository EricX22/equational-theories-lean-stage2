% hard3_0337  eq1=3171 eq2=3667  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(X,Y),f(Y,X)) )).
