% hard3_0343  eq1=3270 eq2=4093  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(X,f(X,Z))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(f(Y,Y),Y),X) )).
