% hard3_0336  eq1=3171 eq2=99  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(goal, conjecture, ! [X] : ( X = f(X,f(f(X,X),X)) )).
