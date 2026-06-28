% hard3_0118  eq1=947 eq2=3126  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,X),f(Y,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Y),X) )).
