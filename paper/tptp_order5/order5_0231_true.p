% order5_0231  eq1=7792 eq2=38449  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,f(Z,Y)),X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(f(Y,Z),X)),X),X) )).
