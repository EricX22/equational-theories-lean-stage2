% hard3_0141  eq1=1085 eq2=4093  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(X,f(Y,Y)),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(f(Y,Y),Y),X) )).
